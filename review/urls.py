from django.urls import path
from .views import add_review, get_review, delete_review, json_reviews, add_review_mobile, delete_review_mobile
app_name = 'review'

urlpatterns = [
    path('api/add_review/<uuid:restaurant_id>/', add_review, name='add_review'),
    path('api/get_reviews/<uuid:restaurant_id>/', get_review, name='get_reviews'),
    path('api/delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('json_reviews/<uuid:restaurant_id>/', json_reviews, name='json_reviews'),
    path('api/add_review_mobile/<uuid:restaurant_id>/', add_review_mobile, name='add_review_mobile'),
    path('api/delete_review_mobile/<int:review_id>/', delete_review_mobile, name='delete_review_mobile'),
]