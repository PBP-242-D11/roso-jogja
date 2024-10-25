from django.urls import path

from .views import (
    create_order,
    add_food_to_cart,
    clear_cart,
    get_cart_items,
    show_cart,
    remove_item_from_cart,
    update_item_quantity
)

app_name = "order"

urlpatterns = [
    path("api/create_order/", create_order, name="create_order"),
    path('api/add_food_to_cart/<uuid:food_id>/', add_food_to_cart, name='add_food_to_cart'),
    path("api/clear_cart/", clear_cart, name="clear_cart"),
    path("api/cart/", get_cart_items, name="get_cart_items"),
    path("show_cart/", show_cart, name="show_cart"),
    path("api/remove_item_from_cart/<uuid:food_id>/", remove_item_from_cart, name="remove_item_from_cart"),
    path("api/update_item_quantity/<uuid:food_id>/", update_item_quantity, name='update_item_quantity')
]