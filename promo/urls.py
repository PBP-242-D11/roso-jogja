from django.urls import path
from promo.views import promo_home, add_promo, remove_promo, edit_promo, use_promo, promo_details, apply_promo, simulate_promo, mobile_promo_home, mobile_use_promo, mobile_promo_details, mobile_edit_promo, mobile_delete_promo, mobile_add_promo, owned_resto, check_promo_code, find_by_code, tag_promo, remove_promo_usage

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
    path('mobile_promo_home/', mobile_promo_home, name='mobile_promo_home'),
    path('mobile_use_promo/<uuid:restaurant_id>/', mobile_use_promo, name='mobile_use_promo'),
    path('mobile_promo_details/<uuid:promo_id>/', mobile_promo_details, name='mobile_promo_details'),
    path('mobile_edit_promo/<uuid:promo_id>/', mobile_edit_promo, name='mobile_edit_promo'),
    path('mobile_delete_promo/<uuid:promo_id>/', mobile_delete_promo, name='mobile_delete_promo'),
    path('mobile_add_promo/', mobile_add_promo, name='mobile_add_promo'),
    path('owned_resto/', owned_resto, name='owned_resto'),
    path('check_promo_code/<str:promo_code>/', check_promo_code, name='check_promo_code'),
    path('find_by_code/<str:promo_code>/', find_by_code , name='find_by_code'),
    path('tag_promo/', tag_promo , name='tag_promo'),
    path('remove_promo_usage/', remove_promo_usage, name='remove_promo_usage')
]