from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from django.views.decorators.csrf import csrf_exempt


from .models import Order, Cart, Food

@require_POST
@csrf_exempt
@login_required
@role_required(['C'])
def create_order(request):
    order = Order.objects.create(
        user= request.user,
        restaurant= request.user.cart.restaurant,
        notes= request.POST.get("notes"),
        payment_method=request.POST.get("payment_method"),
        total_price=request.user.cart.total_price()
    )

    order.save()

    return HttpResponse(b"Order Created Succesfully", status=201)

@require_POST
@csrf_exempt
@login_required
@role_required(['C'])
def create_cart(request):
    user_cart = Cart.objects.create(user=request.user)
    user_cart.save()

    return HttpResponse(b"Cart Created Succesfully", status=201)

@require_POST
@csrf_exempt
@login_required
@role_required(["C"])
def add_food_to_cart(request):
    food_id = request.POST.get("food_id")
    food = Food.objects.get(id=food_id)

    cart = request.user.cart
    cart.add_food(food)

    return HttpResponse(b"Food added successfully", status=201)

@require_http_methods(["DELETE"])
@csrf_exempt
@login_required
@role_required(["C"])
def clear_cart(request):
    user_cart = request.user.cart

    user_cart.foods.clear()
    user_cart.restaurant = None
    user_cart.save()

    return HttpResponse("Successfully cleared the cart", status=200)
