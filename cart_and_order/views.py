import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from common.decorators import role_required

from .models import Cart, CartItem, Food, Order, OrderItem


@require_POST
@csrf_exempt
@login_required
@role_required(["C"])
def create_order(request):
    cart = request.user.get_or_create_cart

    if not cart.cart_items.exists():
        return HttpResponse("Cart is empty", status=400)

    try:
        data = json.loads(request.body)
        notes = data.get("notes", "")
        payment_method = data.get("payment_method")
        final_price = data.get("final_price", 0)
        discount = cart.total_price - final_price
        if discount == cart.total_price:
            discount = 0

        if not payment_method:
            return HttpResponse("Payment method is required", status=400)

        # First create order without total_price
        order = Order.objects.create(
            user=request.user,
            restaurant=cart.restaurant,
            notes=notes,
            payment_method=payment_method,
            total_price=final_price,  # Set initial total_price as final_price, if 0 then update in calculate price
            promo_cut=discount,
        )

        # Create all order items
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                food=cart_item.food,
                quantity=cart_item.quantity,
                price_at_order=cart_item.food.price,
            )

        if order.total_price == 0:
            order.total_price = order.calculate_total_price

        order.save()
        order.refresh_from_db()

        cart.cart_items.all().delete()
        cart.restaurant = None
        cart.save()

        return HttpResponse("Order Created Successfully", status=201)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON data", status=400)


@login_required
@role_required(["C"])
def add_food_to_cart(request, food_id):
    food = Food.objects.get(id=food_id)

    cart = request.user.get_or_create_cart
    quantity = int(request.POST.get("quantity", 1))

    try:
        cart.add_food(food, quantity=quantity)
    except ValueError as e:
        return HttpResponse(str(e), status=400)

    return HttpResponse(b"Food added successfully", status=200)


@require_http_methods(["DELETE"])
@csrf_exempt
@login_required
@role_required(["C"])
def clear_cart(request):
    user_cart = request.user.get_or_create_cart

    user_cart.cart_items.all().delete()
    user_cart.restaurant = None
    user_cart.save()

    return HttpResponse("Successfully cleared the cart", status=200)


@login_required
@role_required(["C"])
def show_cart(request):
    cart = request.user.get_or_create_cart
    cart_items = cart.cart_items.all()
    total_price = cart.total_price

    context = {
        "cart_items": cart_items,
        "username": cart.user.username,
        "restaurant": cart.restaurant,
        "total_price": total_price,
    }
    return render(request, "cart.html", context)


def get_cart_items(request):
    cart = request.user.get_or_create_cart
    cart_items = cart.cart_items.all()

    items = {
        "total": cart.total_price,
        "restaurant": (
            {
                "name": cart.restaurant.name if cart.restaurant else None,
                "id": cart.restaurant.id if cart.restaurant else None,
            }
            if cart.restaurant
            else None
        ),
        "items": [
            {
                "id": item.food.id,
                "name": item.food.name,
                "price": item.food.price,
                "quantity": item.quantity,
            }
            for item in cart_items
        ],
    }

    return JsonResponse(items, safe=False)


@require_http_methods(["DELETE"])
@csrf_exempt
@login_required
@role_required(["C"])
def remove_item_from_cart(request, food_id):
    cart = request.user.get_or_create_cart
    try:
        cart_item = cart.cart_items.get(food_id=food_id)
        cart_item.delete()
        return HttpResponse("Item removed from cart", status=200)
    except CartItem.DoesNotExist:
        return HttpResponse("Item not found in cart", status=404)


@require_http_methods(["PATCH"])
@csrf_exempt
@login_required
@role_required(["C"])
def update_item_quantity(request, food_id):
    cart = request.user.get_or_create_cart
    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        cart_item = cart.cart_items.get(food_id=food_id)
        quantity = data["quantity"]
        if quantity == 0:
            cart_item.delete()
            if cart.total_item == 0:
                cart.restaurant = None
                cart.save()
            return HttpResponse("Item remove successfully", status=200)
        cart_item.quantity = data["quantity"]
        cart_item.save()
        return HttpResponse("Item quantity updated successfully", status=200)
    except CartItem.DoesNotExist:
        return HttpResponse("Item not found in cart", status=404)


@login_required
@role_required(["C"])
def show_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    total_orders = orders.count()
    total_spent = sum(order.total_price for order in orders)
    context = {
        "orders": orders,
        "username": request.user.username,
        "total_orders": total_orders,
        "total_spent": total_spent,
    }
    return render(request, "order_history.html", context)


# FLUTTER


@login_required
@require_GET
def show_order_flutter(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    total_orders = orders.count()
    total_spent = str(sum(order.total_price for order in orders))

    response = {
        "total_order": total_orders,
        "total_spent": total_spent,
        "orders": [
            {
                "id": str(order.order_id),
                "notes": order.notes,
                "payment_method": str(order.payment_method),
                "total_price": str(order.total_price),
                "created_at": order.created_at.strftime("%d %B %Y %H:%M"),
                "promo_cut": str(order.promo_cut),
                "restaurant": order.restaurant.name,
                "order_items": [
                    {
                        "food_name": item.food.name,
                        "quantity": str(item.quantity),
                        "price_at_order": str(item.price_at_order),
                    }
                    for item in OrderItem.objects.filter(order=order)
                ],
            }
            for order in orders
        ],
    }

    return JsonResponse(response, safe=False)


@login_required
@require_GET
def show_cart_flutter(request):
    cart = request.user.get_or_create_cart
    cart_items = cart.cart_items.all()

    response = {
        "total": str(cart.total_price),
        "restaurant": (
            {
                "name": cart.restaurant.name if cart.restaurant else None,
                "id": cart.restaurant.id if cart.restaurant else None,
            }
            if cart.restaurant
            else None
        ),
        "items": [
            {
                "id": str(item.food.id),
                "name": item.food.name,
                "price": item.food.price,
                "quantity": item.quantity,
            }
            for item in cart_items
        ],
    }

    return JsonResponse(response, safe=False)


# add food to cart
@csrf_exempt
@login_required
def add_food_to_cart_api(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get("quantity", 1))

    try:
        cart.add_food(food, quantity=quantity)
        return JsonResponse({"message": "Food added successfully"}, status=200)
    except ValueError as e:
        return JsonResponse({"error": "Food cannot be added to cart"}, status=400)


@csrf_exempt
@login_required
def clear_cart_api(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.cart_items.all().delete()
    cart.restaurant = None
    cart.save()
    return JsonResponse({"message": "Successfully cleared the cart"}, status=200)


@csrf_exempt
@login_required
def remove_food_from_cart_api(request, food_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    try:
        cart_item = cart.cart_items.get(food_id=food_id)
        cart_item.delete()
        return JsonResponse({"message": "Item removed from cart"}, status=200)
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Item not found in cart"}, status=404)


@csrf_exempt
@login_required
@require_GET
def update_food_quantity_api(request, food_id):
    quantity = request.GET.get("quantity")
    if quantity is None:
        return JsonResponse({"error": "Quantity is required"}, status=400)
    try:
        quantity = int(quantity)
        if quantity < 0:
            return JsonResponse({"error": "Invalid quantity"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Quantity must be an integer"}, status=400)

    cart, created = Cart.objects.get_or_create(user=request.user)

    try:
        cart_item = cart.cart_items.get(food_id=food_id)
        if quantity == 0:
            cart_item.delete()
            if cart.cart_items.count() == 0:
                cart.restaurant = None
                cart.save()
            return JsonResponse({"message": "Item removed successfully"}, status=200)
        else:
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse(
                {
                    "message": "Item quantity updated successfully",
                    "cart_item": {
                        "food_id": cart_item.food.id,
                        "food_name": cart_item.food.name,
                        "quantity": cart_item.quantity,
                        "price_at_order": str(cart_item.food.price),
                    },
                },
                status=200,
            )
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Item not found in cart"}, status=404)


@csrf_exempt
@login_required
@role_required(["C"])
def create_order_api(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.cart_items.exists():
        return JsonResponse({"status": "error", "message": "Cart is empty"}, status=400)

    try:
        data = json.loads(request.body)
        notes = data.get("notes", "")
        payment_method = data.get("payment_method")
        final_price = data.get("final_price", 0)
        discount = cart.total_price - final_price
        if discount == cart.total_price:
            discount = 0

        if not payment_method:
            return JsonResponse(
                {"status": "error", "message": "Payment method is required"}, status=400
            )

        order = Order.objects.create(
            user=request.user,
            restaurant=cart.restaurant,
            notes=notes,
            payment_method=payment_method,
            total_price=final_price,
            promo_cut=discount,
        )

        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                food=cart_item.food,
                quantity=cart_item.quantity,
                price_at_order=cart_item.food.price,
            )

        if order.total_price == 0:
            order.total_price = order.calculate_total_price

        order.save()
        order.refresh_from_db()

        cart.cart_items.all().delete()
        cart.restaurant = None
        cart.save()

        return JsonResponse(
            {"status": "success", "message": "Order Created Successfully"}, status=201
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON data"}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": "Failed to create order"}, status=500
        )

