from django.urls import path

from .views import (
    create_food,
    create_restaurant,
    delete_food,
    delete_restaurant,
    restaurant_detail,
    restaurant_list,
    show_delete_food,
    show_delete_restaurant,
    show_restaurant_detail,
    show_restaurants,
    show_update_food,
    show_update_restaurant,
    update_food,
    update_restaurant,
)

app_name = "restaurant"

urlpatterns = [
    path("", show_restaurants, name="show_restaurants"),
    path("<uuid:id>/", show_restaurant_detail, name="show_restaurant_detail"),
    path("delete/<uuid:id>/", show_delete_restaurant, name="delete_restaurant"),
    path("update/<uuid:id>/", show_update_restaurant, name="update_restaurant"),
    path(
        "<uuid:restaurant_id>/delete_food/<uuid:food_id>/",
        show_delete_food,
        name="delete_food",
    ),
    path(
        "<uuid:restaurant_id>/update_food/<uuid:food_id>/",
        show_update_food,
        name="update_food",
    ),
    path("api/restaurants/", restaurant_list, name="restaurant_list"),
    path("api/restaurants/create/", create_restaurant, name="create_restaurant"),
    path(
        "api/restaurants/delete/<uuid:id>/", delete_restaurant, name="delete_restaurant"
    ),
    path(
        "api/restaurants/update/<uuid:id>/", update_restaurant, name="update_restaurant"
    ),
    path("api/restaurants/<uuid:id>/", restaurant_detail, name="restaurant_detail"),
    path("api/restaurants/<uuid:id>/create_food/", create_food, name="create_food"),
    path(
        "api/restaurants/<uuid:restaurant_id>/delete_food/<uuid:food_id>/",
        delete_food,
        name="delete_food",
    ),
    path(
        "api/restaurants/<uuid:restaurant_id>/update_food/<uuid:food_id>/",
        update_food,
        name="update_food",
    ),
]
