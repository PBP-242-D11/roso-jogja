from django.urls import path
from promo.views import promo_home, add_promo, remove_promo, edit_promo, use_promo, promo_details, apply_promo, simulate_promo

app_name = 'promo'

urlpatterns = [
    path('', promo_home, name='promo_home'),
    path('add_promo/', add_promo, name='add_promo'),
    path('edit_promo/<uuid:promo_id>/', edit_promo, name='edit_promo'),
    path('remove_promo/<uuid:promo_id>/', remove_promo, name='remove_promo'),
    path('use_promo/<uuid:restaurant_id>/', use_promo, name='use_promo'),
    path('details/<uuid:promo_id>/', promo_details, name='promo_details'),
    path('apply_promo/', apply_promo, name='apply_promo'),
    path('simulate_promo/', simulate_promo, name='simulate_promo'),
]