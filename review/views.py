from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Review
from restaurant.models import Restaurant
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from cart_and_order.models import Order 


@csrf_exempt
@login_required
@require_POST
@csrf_exempt
@login_required
@require_POST
def add_review(request, restaurant_id):
    user = request.user
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Memeriksa apakah pengguna memiliki pesanan dari restoran ini
    user_orders = Order.objects.filter(user=user, restaurant=restaurant)
    if not user_orders.exists():
        return JsonResponse({"error": "You need to order from this restaurant before leaving a review."}, status=403)

    # Melanjutkan untuk memproses review jika pengguna memiliki pesanan
    data = request.POST
    rating = data.get("rating")
    comment = data.get("comment", "")

    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        return JsonResponse({"error": "Invalid rating."}, status=400)

    review = Review.objects.create(
        restaurant=restaurant,
        user=user,
        rating=int(rating),
        comment=comment
    )

    return JsonResponse({
        "success": True,
        "review": {
            "user": user.first_name,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.strftime("%B %d, %Y, %I:%M %p")
        }
    })

def get_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant).select_related('user')
    reviews_data = [
        {
            'id': review.id,
            "user": review.user.username,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.strftime("%B %d, %Y, %I:%M %p")
        }
        for review in reviews
    ]
    return JsonResponse({"reviews": reviews_data})

@csrf_exempt
def delete_review(request, review_id):
    if request.method == "DELETE":
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
