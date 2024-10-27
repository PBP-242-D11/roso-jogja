from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.urls import reverse
import json

from .models import Order, Cart, CartItem, Food, OrderItem


@require_POST
@csrf_exempt
@login_required
@role_required(['C'])
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
            promo_cut=discount
        )

        # Create all order items
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                food=cart_item.food,
                quantity=cart_item.quantity,
                price_at_order=cart_item.food.price
            )
        
        # Now update the order's total price manually after all items are created
        if order.total_price == 0:
            order.total_price = order.calculate_total_price
        order.save()
        order.refresh_from_db() 

        # Clear the cart after the order is created
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
    quantity = int(request.POST.get("quantity", 1))  # Tambahkan kuantitas dari POST request

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

    # Hapus semua item dari keranjang
    user_cart.cart_items.all().delete()
    user_cart.restaurant = None
    user_cart.save()

    return HttpResponse("Successfully cleared the cart", status=200)

@login_required
@role_required(['C'])
def show_cart(request):
    cart = request.user.get_or_create_cart
    cart_items = cart.cart_items.all()  # Ambil item-item dari keranjang
    total_price = cart.total_price  # Hitung total harga dari item-item di keranjang
    

    context = {
        'cart_items': cart_items,  # Gunakan cart_items sebagai pengganti foods
        'username': cart.user.username,
        'restaurant': cart.restaurant,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def get_cart_items(request):
    cart = request.user.get_or_create_cart
    cart_items = cart.cart_items.all()  # Ambil item-item dari keranjang

    items = {
        "total": cart.total_price,
        "restaurant": {
            "name": cart.restaurant.name if cart.restaurant else None,
            "id":cart.restaurant.id if cart.restaurant else None,
        } if cart.restaurant else None,
        "items":[
                {
                'id': item.food.id,
                'name': item.food.name,
                'price': item.food.price,
                'quantity': item.quantity,
            }
            for item in cart_items
        ]
    }

    return JsonResponse(items, safe=False)  # Kembalikan item dalam format JSON

@require_http_methods(["DELETE"])
@csrf_exempt
@login_required
@role_required(["C"])
def remove_item_from_cart(request, food_id):
    cart = request.user.get_or_create_cart
    try:
        cart_item = cart.cart_items.get(food_id=food_id)
        cart_item.delete()  # Hapus item dari keranjang
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
        data = json.loads(request.body)  # `request.body` contains the raw request body in bytes

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
@role_required(['C'])
def show_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'username': request.user.username,
    }
    return render(request, 'order_history.html', context)

