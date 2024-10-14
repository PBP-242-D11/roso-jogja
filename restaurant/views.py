from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Restaurant


# Create your views here.
@require_GET
def restaurant_list(request):
    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 10)

    try:
        page_size = int(page_size)
        page_size = max(1, min(100, page_size))
    except ValueError:
        page_size = 10

    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, page_size)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    restaurant_data = [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "slug": restaurant.slug,
            "description": restaurant.description,
            "address": restaurant.address,
            "price_range": restaurant.price_range,
        }
        for restaurant in page_obj
    ]

    return JsonResponse(
        {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "results": restaurant_data,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        }
    )


def show_restaurants(request):
    return render(request, "restaurant_list.html")
