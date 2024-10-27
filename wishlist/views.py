from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist, Restaurant
from django.http import JsonResponse, HttpResponseBadRequest

@login_required
def wishlist_view(request):
    """View untuk menampilkan daftar wishlist pengguna."""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("restaurant")
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def add_to_wishlist(request, restaurant_id):
    """View untuk menambah restoran ke wishlist pengguna."""
    if request.method == "POST":
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, restaurant=restaurant)
        return JsonResponse({
            'created': created,
            'restaurant_name': restaurant.name,
        })
    else:
        # Jika request bukan POST, berikan respons error
        return HttpResponseBadRequest("Only POST requests are allowed for adding items to the wishlist.")

@login_required
def remove_from_wishlist(request, restaurant_id):
    """View untuk menghapus restoran dari wishlist pengguna."""
    if request.method == "POST":
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, restaurant_id=restaurant_id)
            wishlist_item.delete()
            return JsonResponse({'deleted': True})
        except Wishlist.DoesNotExist:
            return JsonResponse({'deleted': False, 'error': 'Item not found in wishlist'}, status=404)

def wishlist_status(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('restaurant_id', flat=True)
        return JsonResponse(list(wishlist_items), safe=False)
    return JsonResponse([], safe=False)















































































































































































































