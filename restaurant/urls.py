from django.urls import path

from .views import restaurant_list, show_restaurants

app_name = "restaurant"

urlpatterns = [
    path("", show_restaurants, name="show_restaurants"),
    path("api/restaurants/", restaurant_list, name="restaurant_list"),
]
