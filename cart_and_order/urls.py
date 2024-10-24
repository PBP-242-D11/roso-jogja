from django.urls import path

from .views import (
    create_order,
    add_food_to_cart,
    clear_cart,
    show_cart
)

app_name = "order"

urlpatterns = [
    path("api/create_order/", create_order, name="create_order"),
    path('api/add_food_to_cart/<uuid:food_id>/', add_food_to_cart, name='add_food_to_cart'),
    path("api/clear_cart/", clear_cart, name="clear_cart"),
    path("show_cart/", show_cart, name="show_cart")
]
