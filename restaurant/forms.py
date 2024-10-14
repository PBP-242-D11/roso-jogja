from django import forms
from django.forms import ModelForm

from .models import Restaurant


class RestaurantForm(ModelForm):

    class Meta:
        model = Restaurant
        fields = ["name", "price_range", "address", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
