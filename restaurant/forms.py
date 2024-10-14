from django import forms
from django.forms import ModelForm

from .models import Restaurant


class RestaurantForm(ModelForm):

    class Meta:
        model = Restaurant
        fields = ["name", "price_range", "address", "description"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 2}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
