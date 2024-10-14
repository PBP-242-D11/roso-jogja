from django.urls import path

from .views import (
    restaurant_detail,
    restaurant_list,
    show_restaurant_detail,
    show_restaurants,
)

app_name = "restaurant"

urlpatterns = [
    path("", show_restaurants, name="show_restaurants"),
    path("<uuid:id>/", show_restaurant_detail, name="show_restaurant_detail"),
    path("api/restaurants/", restaurant_list, name="restaurant_list"),
    path("api/restaurants/<uuid:id>/", restaurant_detail, name="restaurant_detail"),
]
