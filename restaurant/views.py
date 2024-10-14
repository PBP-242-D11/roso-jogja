from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from common.decorators import role_required

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
    if (request.user.is_authenticated) and (request.user.role == "R"):
        restaurants = restaurants.filter(owner=request.user)

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


@require_GET
def restaurant_detail(request, id):
    restaurant = Restaurant.objects.get(id=id)
    foods = restaurant.foods.all()

    return JsonResponse(
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "description": restaurant.description,
            "address": restaurant.address,
            "price_range": restaurant.price_range,
            "foods": [
                {
                    "id": food.id,
                    "name": food.name,
                    "description": food.description,
                    "price": food.price,
                }
                for food in foods
            ],
        }
    )


@require_POST
@csrf_exempt
@login_required(login_url="/login/")
@role_required(allowed_roles=["R"])
def create_restaurant(request):
    name = request.POST.get("name")
    address = request.POST.get("address")
    price_range = request.POST.get("price-range")
    description = request.POST.get("description")

    owner = request.user

    new_restaurant = Restaurant.objects.create(
        name=name,
        address=address,
        price_range=price_range,
        description=description,
        owner=owner,
    )

    new_restaurant.save()

    return HttpResponse(b"Restaurant created successfully", status=201)


def show_restaurant_detail(request, id):
    return render(request, "restaurant_detail.html")


def show_restaurants(request):
    return render(request, "restaurant_list.html")


def show_my_restaurants(request):
    return render(request, "my_restaurants.html")
