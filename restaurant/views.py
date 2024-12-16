from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from common.decorators import role_required

from .forms import FoodForm, RestaurantForm
from .models import Restaurant


# Create your views here.
@require_GET
def restaurant_list(request):
    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 10)
    search = request.GET.get("search", None)

    try:
        page_size = int(page_size)
        page_size = max(1, min(100, page_size))
    except ValueError:
        page_size = 10

    if search is None or search == "":
        restaurants = Restaurant.objects.all()
    else:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=search) | Q(categories__icontains=search)
        )
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
            "categories": restaurant.categories,
            "placeholder_image": restaurant.placeholder_image,
        }
        for restaurant in page_obj
    ]

    return JsonResponse(
        {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "page_range": list(paginator.page_range),
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "results": restaurant_data,
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
            "slug": restaurant.slug,
            "description": restaurant.description,
            "address": restaurant.address,
            "categories": restaurant.categories,
            "placeholder_image": restaurant.placeholder_image,
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


@csrf_exempt
@require_POST
@login_required(login_url="/login/")
@role_required(allowed_roles=["R"])
def create_restaurant(request):
    name = request.POST.get("name")
    address = request.POST.get("address")
    categories = request.POST.get("categories")
    description = request.POST.get("description")

    owner = request.user

    new_restaurant = Restaurant.objects.create(
        name=name,
        address=address,
        categories=categories,
        description=description,
        owner=owner,
    )

    new_restaurant.save()

    return JsonResponse({"status": "success"}, status=201)


@login_required(login_url="/login/")
@role_required(allowed_roles=["R"])
def show_delete_restaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()

    return HttpResponseRedirect(
        reverse("restaurant:show_restaurants"), {"status": "success"}
    )


@login_required(login_url="/login/")
@role_required(allowed_roles=["R"])
def show_update_restaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)

    form = RestaurantForm(request.POST or None, instance=restaurant)

    if form.is_valid() and request.method == "POST":
        form.save()

        return HttpResponseRedirect(reverse("restaurant:show_restaurants"))

    return render(request, "restaurant_update.html", {"form": form})


@require_POST
@login_required(login_url="/login/")
@role_required(allowed_roles=["R"])
def create_food(request, id):
    restaurant = Restaurant.objects.get(id=id)
    if restaurant.owner != request.user:
        return HttpResponse(b"Unauthorized", status=401)

    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")

    new_food = restaurant.foods.create(name=name, price=price, description=description)
    new_food.save()

    return JsonResponse({"status": "success"}, status=201)


@login_required(login_url="/login/")
@role_required(allowed_roles=["R"])
def show_delete_food(request, restaurant_id, food_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if restaurant.owner != request.user:
        return HttpResponse(b"Unauthorized", status=401)

    food = restaurant.foods.get(id=food_id)

    food.delete()

    return HttpResponseRedirect(
        reverse("restaurant:show_restaurant_detail", args=[restaurant_id])
    )


@login_required(login_url="/login/")
@role_required(allowed_roles=["R"])
def update_food(request, restaurant_id, food_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if restaurant.owner != request.user:
        return HttpResponse(b"Unauthorized", status=401)

    food = restaurant.foods.get(id=food_id)

    form = FoodForm(request.POST or None, instance=food)

    if form.is_valid() and request.method == "POST":
        form.save()

        return HttpResponseRedirect(
            reverse("restaurant:show_restaurant_detail", args=[restaurant_id])
        )

    return render(request, "restaurant_food_update.html", {"form": form})


def show_restaurant_detail(request, id):
    restaurant = Restaurant.objects.get(id=id)

    context = {
        "restaurant_id": id,
        "restaurant_form": RestaurantForm(request.POST or None, instance=restaurant),
        "food_form": FoodForm(),
    }
    return render(request, "restaurant_detail.html", context)


def show_restaurants(request):
    context = {"form": RestaurantForm()}
    return render(request, "restaurant_list.html", context)


# Mobile API ===================================================================


@csrf_exempt
@login_required
@role_required(allowed_roles=["R"])
def delete_restaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()

    return JsonResponse({"status": "success"}, status=200)


@csrf_exempt
@require_POST
@login_required
@role_required(allowed_roles=["R"])
def update_restaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)

    form = RestaurantForm(request.POST or None, instance=restaurant)

    if form.is_valid() and request.method == "POST":
        form.save()

        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"status": "failed"}, status=400)


@csrf_exempt
@require_POST
@login_required
@role_required(allowed_roles=["R"])
def create_food(request, id):
    restaurant = Restaurant.objects.get(id=id)
    if restaurant.owner != request.user:
        return JsonResponse({"status": "failed"}, status=401)

    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")

    new_food = restaurant.foods.create(name=name, price=price, description=description)
    new_food.save()

    return JsonResponse({"status": "success"}, status=201)


@csrf_exempt
@login_required
@role_required(allowed_roles=["R"])
def delete_food(request, restaurant_id, food_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if restaurant.owner != request.user:
        return JsonResponse({"status": "failed"}, status=401)

    food = restaurant.foods.get(id=food_id)

    food.delete()

    return JsonResponse({"status": "success"}, status=200)
