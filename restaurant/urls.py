from django.urls import path

from .views import (
    create_restaurant,
    delete_restaurant,
    restaurant_detail,
    restaurant_list,
    show_restaurant_detail,
    show_restaurants,
    update_restaurant,
)

app_name = "restaurant"

urlpatterns = [
    path("", show_restaurants, name="show_restaurants"),
    path("<uuid:id>/", show_restaurant_detail, name="show_restaurant_detail"),
    path("delete/<uuid:id>/", delete_restaurant, name="delete_restaurant"),
    path("update/<uuid:id>/", update_restaurant, name="update_restaurant"),
    path("api/restaurants/", restaurant_list, name="restaurant_list"),
    path("api/restaurants/create/", create_restaurant, name="create_restaurant"),
    path("api/restaurants/<uuid:id>/", restaurant_detail, name="restaurant_detail"),
]
