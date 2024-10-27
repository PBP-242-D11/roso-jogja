from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from promo.models import Promo
from restaurant.models import Restaurant
from cart_and_order.models import Cart
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from promo.forms import PromoForm
import uuid
import json
from datetime import date
from django.http import JsonResponse
from common.decorators import role_required
from django.contrib.auth.decorators import login_required

@login_required
def promo_home(request):
    other_promos = ""
    if request.user.role == "A":
        promos = Promo.objects.all()
    elif request.user.role == "R":
        owned_restaurants = Restaurant.objects.filter(owner=request.user)
        other_promos = Promo.objects.all().exclude(user=request.user).distinct()
        promos = Promo.objects.filter(user=request.user)
    else:
        promos = Promo.objects.filter(shown_to_public=True)
    context = {
        'promos': promos,
        'other_promos': other_promos,
        'message': 'No promos available' if not promos and not other_promos else ''
    }
    return render(request, 'promo_home.html', context)

@login_required
@role_required(allowed_roles=["C"])
def use_promo(request, restaurant_id):
    other_promos = ""
    # Uncomment kalo udah fully implement cart and order
    cart = get_object_or_404(Cart, user=request.user) # Asumsinya ngambil data order dari cart
    total_price = float(cart.total_price)
    print(total_price)
    promos = Promo.objects.filter(
        shown_to_public=True,
        min_payment__lte=total_price,
        expiry_date__gte=date.today(),
        restaurant=restaurant_id,
    ).exclude(max_usage=0)
    other_promos = Promo.objects.filter(
        shown_to_public=True,
        min_payment__gt=total_price,
        expiry_date__gte=date.today(),
        restaurant=restaurant_id,
    ).exclude(max_usage=0)
    # promos = Promo.objects.filter(shown_to_public=True,
    #     expiry_date__gte=date.today(),
    #     restaurant=restaurant_id).exclude(max_usage=0)
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code')
        promo_id = request.POST.get('promo_id')
        try:
            promo = Promo.objects.filter(promo_code=promo_code, restaurant=restaurant_id).first()
            if promo.min_payment > total_price or promo.expiry_date < date.today():
                promo=""
                return JsonResponse({'status': 'error', 'message': "Requirements not met to use this promo."})
            if not promo and promo_id:
                promo = Promo.objects.filter(id=promo_id).first()
        except:
            promo=""
        
        if promo:
            return JsonResponse({'status': 'success', 'message': f"Promo applied!", 'promo_id': promo.id})
        else:
            return JsonResponse({'status': 'error', 'message': "Invalid promo code."})
    
    context = {
        'promos': promos,
        'other_promos': other_promos,
        'message': 'No promos available. Try entering a promo code instead.' if not promos else '',
        'restaurant_id': restaurant_id
    }
    return render(request, 'use_promo.html', context)

@login_required
@role_required(allowed_roles=["R", "A"])
def add_promo(request):
    if request.user.role == "A":
        restaurant_queryset = Restaurant.objects.all()
    elif request.user.role == "R":
        restaurant_queryset = Restaurant.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        form = PromoForm(request.POST, restaurant_queryset=restaurant_queryset)
        
        if form.is_valid():
            promo = form.save(commit=False)
            promo.user = request.user
            promo.save()
            
            selected_restaurant = request.POST.getlist('restaurant')
            if selected_restaurant:
                for restaurant_id in selected_restaurant:
                    try:
                        restaurant_obj = Restaurant.objects.get(pk=restaurant_id)
                        promo.restaurant.add(restaurant_obj)
                    except Restaurant.DoesNotExist:
                        form.add_error('restaurant', 'Invalid restaurant selected.')
            else:
                form.add_error('restaurant', 'At least one restaurant must be selected.')
            
            promo.save()
            return redirect('/promo')
    
    else:
        form = PromoForm(restaurant_queryset=restaurant_queryset)  # Reinisialisasi form kalau get request saja (untuk allow pesan error seen)
    
    context = {
        'restaurant': restaurant_queryset,
        'form': form,  # Pass kembali form dengan errornya
    }
    return render(request, 'add_promo.html', context)


@login_required
@role_required(allowed_roles=["R", "A"])
def edit_promo(request, promo_id):
    if request.user.role == "A":
        restaurant_queryset = Restaurant.objects.all()
    elif request.user.role == "R":
        restaurant_queryset = Restaurant.objects.filter(owner=request.user)
    promo = get_object_or_404(Promo, id=promo_id)
    
    if request.method == 'POST':
        form = PromoForm(request.POST, instance=promo, restaurant_queryset=restaurant_queryset)
        if form.is_valid():
            form.save()
            return redirect('/promo')
    
    else:
        form = PromoForm(instance=promo, restaurant_queryset=restaurant_queryset)
    
    context = {
        'restaurant': restaurant_queryset,
        'form': form,
        'promo': promo,
    }
    return render(request, 'edit_promo.html', context)

@login_required
@role_required(allowed_roles=["R", "A"])
def remove_promo(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id)
    promo.delete()
    return redirect('/promo')

@login_required
def promo_details(request, promo_id):
    try:
        promo = Promo.objects.get(id=promo_id)
        restaurants = promo.restaurant.values_list('name', flat=True)
        data = {
            'promo_code': promo.promo_code,
            'type': promo.type,
            'value': promo.value,
            'min_payment': promo.min_payment,
            'expiry_date': promo.expiry_date,
            'restaurants': list(restaurants)
        }
        return JsonResponse(data)
    except Promo.DoesNotExist:
        return JsonResponse({'error': 'Promo not found'}, status=404)
    
@require_POST
@login_required
@csrf_exempt
def apply_promo(request):
    data = json.loads(request.body)
    promo_id = data.get("promo_id")
    payment = data.get("payment")
    restaurant_id = data.get("restaurant_id")

    try:
        promo = Promo.objects.get(id=promo_id)
        
        new_price = promo.use_promo(payment, restaurant_id)

        if new_price < 0:
            error_messages = {
                -3: "Promo expired",
                -4: "Invalid restaurant",
                -1: "Minimum payment not met",
                0: "Promo usage limit reached",
                -2: "Unknown error"
            }
            return JsonResponse({"error_message": error_messages.get(new_price, "Promo error")}, status=400)

        return JsonResponse({"new_price": new_price, "promo_value": promo.value, "promo_type": promo.type}, status=200)
    except Promo.DoesNotExist:
        return JsonResponse({"error_message": "Promo not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error_message": str(e)}, status=500)

@require_POST
@login_required
@csrf_exempt
def simulate_promo(request):
    data = json.loads(request.body)
    promo_id = data.get("promo_id")
    payment = data.get("payment")
    restaurant_id = data.get("restaurant_id")

    try:
        promo = Promo.objects.get(id=promo_id)
        
        new_price = promo.simulate_promo(payment, restaurant_id)

        if new_price < 0:
            error_messages = {
                -3: "Promo expired",
                -4: "Invalid restaurant",
                -1: "Minimum payment not met",
                0: "Promo usage limit reached",
                -2: "Unknown error"
            }
            return JsonResponse({"error_message": error_messages.get(new_price, "Promo error")}, status=400)

        return JsonResponse({"new_price": new_price, "promo_value": promo.value, "promo_type": promo.type}, status=200)
    except Promo.DoesNotExist:
        return JsonResponse({"error_message": "Promo not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error_message": str(e)}, status=500)