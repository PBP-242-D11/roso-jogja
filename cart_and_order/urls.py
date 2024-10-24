from django.urls import path

from .views import (
    create_order,
    create_cart,
    add_food_to_cart,
    clear_cart
)

app_name = "restaurant"

urlpatterns = [
    path("api/create_order/", create_order, name="create_order"),
    path('api/create_cart/', create_cart, name="create_cart"),
    path('api/add_food_to_cart/', add_food_to_cart, name='add_food_to_cart'),
    path("api/clear_cart/", clear_cart, name="clear_cart")
]
