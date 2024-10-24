from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Order, Cart, CartItem, Food, OrderItem

@require_POST
@csrf_exempt
@login_required
@role_required(['C'])
def create_order(request):
    cart = request.user.get_or_create_cart

    if not cart.cart_items.exists():
        return HttpResponse(b"Cart is empty", status=400)

    order = Order.objects.create(
        user=request.user,
        restaurant=cart.restaurant,
        notes=request.POST.get("notes"),
        payment_method=request.POST.get("payment_method"),
        total_price=cart.total_price  # total_price diambil dari cart
    )

    # Buat OrderItem untuk setiap item di keranjang
    for cart_item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            food=cart_item.food,
            quantity=cart_item.quantity,
            price_at_order=cart_item.food.price  # harga saat order
        )

    # Kosongkan keranjang setelah order dibuat
    cart.cart_items.all().delete()
    cart.restaurant = None
    cart.save()

    return HttpResponse(b"Order Created Successfully", status=201)


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
