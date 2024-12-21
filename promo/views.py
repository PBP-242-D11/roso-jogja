from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from promo.models import Promo
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from restaurant.models import Restaurant
from cart_and_order.models import Cart
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from promo.forms import PromoForm
import uuid
import json
from django.forms.models import model_to_dict

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

# ============== FOR BACKEND FLUTTER ====================

@csrf_exempt
@login_required
def mobile_promo_home(request):
    other_promos = []
    if request.user.role == "A":
        promos = Promo.objects.all()
    elif request.user.role == "R":
        owned_restaurants = Restaurant.objects.filter(owner=request.user)
        other_promos = Promo.objects.exclude(user=request.user).distinct()
        promos = Promo.objects.filter(user=request.user)
    else:
        promos = Promo.objects.filter(shown_to_public=True)

    # Helper function to serialize promos with restaurants
    def serialize_promo(promo):
        all_restaurants = list(promo.restaurant.values_list('name', flat=True))
        return {
            'id': str(promo.id),
            'user_id': str(promo.user_id),
            'type': promo.type,
            'value': promo.value,
            'min_payment': promo.min_payment,
            'promo_code': promo.promo_code,
            'expiry_date': promo.expiry_date,
            'max_usage': promo.max_usage,
            'shown_to_public': promo.shown_to_public,
            'restaurants': all_restaurants,
        }

    promos_data = [serialize_promo(promo) for promo in promos]
    other_promos_data = [serialize_promo(promo) for promo in other_promos]

    data = {
        'promos': promos_data,
        'other_promos': other_promos_data,
        'message': 'No promos available' if not promos_data and not other_promos_data else '',
    }
    return JsonResponse(data)

@csrf_exempt
@login_required
@role_required(allowed_roles=["C"])
def find_by_code(request, promo_code):
    if request.method == 'GET':
        try:
            promo = Promo.objects.filter(promo_code=promo_code).first()
            if not promo:
                return JsonResponse({'error': 'Promo not found'}, status=404)

            data = {
                'promo': {
                    'id': promo.id,
                    'promo_code': promo.promo_code,
                    'value': promo.value,
                    'expiry_date': promo.expiry_date,
                }
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
@role_required(allowed_roles=["C"])
def mobile_use_promo(request, restaurant_id): # use promo page
    if request.method == 'GET':
        try:
            cart = get_object_or_404(Cart, user=request.user)
            total_price = float(cart.total_price)
            promos = list(Promo.objects.filter(
                shown_to_public=True,
                min_payment__lte=total_price,
                expiry_date__gte=date.today(),
                restaurant=restaurant_id
            ).exclude(max_usage=0).values())
            other_promos = list(Promo.objects.filter(
                shown_to_public=True,
                min_payment__gt=total_price,
                expiry_date__gte=date.today(),
                restaurant=restaurant_id
            ).exclude(max_usage=0).values())
            data = {
                'promos': promos,
                'other_promos': other_promos,
                'message': 'Enter a promo code if none are available.',
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found'}, status=404)
    # Implement POST method if needed
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
def tag_promo(request):
    try:
        promo_id = request.GET.get('promo_id')

        if not promo_id:
            return JsonResponse({'error': 'Promo ID is required'}, status=400)

        promo = Promo.objects.filter(id=promo_id).first()
        if not promo:
            return JsonResponse({'error': 'Promo not found'}, status=404)

        if promo.max_usage == 0:
            return JsonResponse({'error': 'Promo usage limit reached'}, status=400)
        if promo.expiry_date < date.today():
            return JsonResponse({'error': 'Promo has expired'}, status=400)

        user = request.user
        cart = get_object_or_404(Cart, user=request.user)
        cart.promo = promo_id

        promo.max_usage -= 1
        promo.save()
        cart.save()

        return JsonResponse({'status': 'success', 'message': 'Promo tagged successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@login_required
def remove_promo_usage(request):
    try:
        cart = get_object_or_404(Cart, user=request.user)
        cart.promo = ""
        cart.save() 

        return JsonResponse({'status': 'success', 'message': 'Promo deleted successfully.'})
    except Promo.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Promo not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@csrf_exempt
@login_required
def mobile_promo_details(request, promo_id):
    try:
        promo = Promo.objects.get(id=promo_id)
        data = {
            'id': promo.id,
            'user_id': promo.user.id,
            'type': promo.type,
            'value': promo.value,
            'min_payment': promo.min_payment,
            'promo_code': promo.promo_code,
            'expiry_date': str(promo.expiry_date),
            'max_usage': promo.max_usage,
            'shown_to_public': promo.shown_to_public,
            'restaurants': list(promo.restaurant.values_list('name', flat=True))
        }
        return JsonResponse(data)
    except Promo.DoesNotExist:
        return JsonResponse({'error': 'Promo not found'}, status=404)

@csrf_exempt
@login_required
@role_required(allowed_roles=["R"])
def mobile_add_promo(request):
    promo_type = request.POST.get("type")
    value = request.POST.get("value")
    min_payment = request.POST.get("min_payment")
    restaurant_ids = request.POST.get("restaurants", "")
    selected_restaurant = restaurant_ids.split(",") if restaurant_ids else []
    promo_code = request.POST.get("promo_code")
    expiry_date = request.POST.get("expiry_date")
    max_usage = request.POST.get("max_usage")
    shown_to_public = request.POST.get("shown_to_public")
    if shown_to_public.strip().lower() == "true":
        shown_to_public = True
    else:
        shown_to_public = False
    
    if Promo.objects.filter(promo_code=promo_code).exists():
        return JsonResponse({"status": "error", "message": "Promo code already exists."}, status=400)

    owner = request.user

    new_promo = Promo.objects.create(
        user = owner,
        type = promo_type,
        value = value,
        min_payment = min_payment,
        promo_code = promo_code,
        expiry_date = expiry_date,
        max_usage = max_usage,
        shown_to_public = shown_to_public,
    )
    if selected_restaurant:
        for restaurant_id in selected_restaurant:
            restaurant_obj = Restaurant.objects.get(pk=restaurant_id)
            new_promo.restaurant.add(restaurant_obj)

    new_promo.save()

    return JsonResponse({"status": "success"}, status=201)

@csrf_exempt
@require_POST
@login_required
@role_required(allowed_roles=["R"])
def mobile_edit_promo(request, promo_id):
    promo = Promo.objects.get(id=promo_id)
    promo_type = request.POST.get("type")
    value = request.POST.get("value")
    min_payment = request.POST.get("min_payment")
    restaurant_ids = request.POST.get("restaurants", "")
    selected_restaurant = restaurant_ids.split(",") if restaurant_ids else []
    promo_code = request.POST.get("promo_code")
    expiry_date = request.POST.get("expiry_date")
    max_usage = request.POST.get("max_usage")
    shown_to_public = request.POST.get("shown_to_public")
    if shown_to_public.strip().lower() == "true":
        shown_to_public = True
    else:
        shown_to_public = False
    try:
        promo.type = promo_type
        promo.value = value
        promo.min_payment = min_payment
        if selected_restaurant:
            for restaurant_id in selected_restaurant:
                restaurant_obj = Restaurant.objects.get(pk=restaurant_id)
                if not promo.restaurant.filter(pk=restaurant_obj.pk).exists():
                    promo.restaurant.add(restaurant_obj)
        promo.promo_code = promo_code
        promo.expiry_date = expiry_date
        promo.max_usage = max_usage
        promo.shown_to_public = shown_to_public
        promo.save()
        return JsonResponse({"status": "success"}, status=200)
    except:
        return JsonResponse({"status": "failed"}, status=400)

@csrf_exempt
@login_required
@role_required(allowed_roles=["R"])
def mobile_delete_promo(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id)
    promo.delete()
    return JsonResponse({'status': 'success', 'message': 'Promo deleted successfully'})

@csrf_exempt
@login_required
@role_required(allowed_roles=["R"])
def check_promo_code(request, promo_code):
    if Promo.objects.filter(promo_code=promo_code).exists():
        return JsonResponse({"exists": True}, status=200)
    return JsonResponse({"exists": False}, status=200)

@csrf_exempt
@login_required
@role_required(allowed_roles=["A", "R"])
def owned_resto(request):
    # Query the restaurants owned by the user
    restos = Restaurant.objects.filter(owner=request.user)
    
    # Serialize the queryset into a list of dictionaries
    restos_data = list(restos.values('id', 'name', 'address'))  # Include fields you want in the response
    
    data = {
        'restos': restos_data
    }
    return JsonResponse(data)