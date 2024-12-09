from django.urls import path
from . import views

app_name = 'wishlist'
urlpatterns = [
    path('', views.wishlist_view, name='wishlist_view'),  # URL untuk melihat wishlist
    path('add/<uuid:restaurant_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # URL untuk menambah item ke wishlist
    path('remove/<uuid:restaurant_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # URL untuk menghapus item dari wishlist
    path('wishlist/status/', views.wishlist_status, name='wishlist_status'),
    path('wishlist/status/count/', views.wishlist_count, name='wishlist_count'),  # URL untuk menghitung jumlah wishlist
]