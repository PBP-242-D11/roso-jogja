from django import forms
from django.forms import ModelForm

from .models import Food, Restaurant


class RestaurantForm(ModelForm):

    class Meta:
        model = Restaurant
        fields = ["name", "price_range", "address", "description"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 2}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class FoodForm(ModelForm):

    class Meta:
        model = Food
        fields = ["name", "price", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
