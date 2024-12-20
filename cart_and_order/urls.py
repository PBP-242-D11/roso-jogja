from django.urls import path

from .views import (
    create_order,
    add_food_to_cart,
    clear_cart,
    get_cart_items,
    show_cart,
    remove_item_from_cart,
    update_item_quantity,
    show_orders,
    show_order_flutter,
    show_cart_flutter,
    add_food_to_cart_api,
    remove_food_from_cart_api,
    update_food_quantity_api,
    clear_cart_api,
    create_order_api
)

app_name = "order"

urlpatterns = [
    path("api/create_order/", create_order, name="create_order"),
    path('api/add_food_to_cart/<uuid:food_id>/', add_food_to_cart, name='add_food_to_cart'),
    path("api/clear_cart/", clear_cart, name="clear_cart"),
    path("api/cart/", get_cart_items, name="get_cart_items"),
    path("show_cart/", show_cart, name="show_cart"),
    path("api/remove_item_from_cart/<uuid:food_id>/", remove_item_from_cart, name="remove_item_from_cart"),
    path("api/update_item_quantity/<uuid:food_id>/", update_item_quantity, name='update_item_quantity'),
    path('orders/', show_orders, name='show_order_history'),

    # flutter
    path("api/show_orders/", show_order_flutter, name="order_history"),
    path('api/cart/add/<uuid:food_id>/', add_food_to_cart_api, name='add_food_to_cart_api'),
    path('api/cart/remove/<uuid:food_id>/', remove_food_from_cart_api, name='remove_item_from_cart_api'),
    path('api/cart/update/<uuid:food_id>/', update_food_quantity_api, name='update_item_quantity_api'),
    path('api/cart/clear/', clear_cart_api, name='clear_cart_api'),
    path('api/mobile_cart/', show_cart_flutter, name='get_cart_items_api'),
    path("api/mobile_create_order/", create_order_api, name="create_order_api"),
]