from django import forms
from django.core.exceptions import ValidationError
from .models import Promo
from datetime import date

class PromoForm(forms.ModelForm):
    class Meta:
        model = Promo
        exclude = ['id', 'user']
        widgets = {
            'expiry_date': forms.SelectDateWidget(),
            'restaurant': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        restaurant_queryset = kwargs.pop('restaurant_queryset', None)
        super(PromoForm, self).__init__(*args, **kwargs)
        
        if restaurant_queryset is not None:
            self.fields['restaurant'].queryset = restaurant_queryset

    def clean_type(self):
        promo_type = self.cleaned_data.get('type')
        if promo_type not in ['Percentage', 'Fixed Price']:
            raise ValidationError("Promo type must be either 'Percentage' or 'Fixed Price'.")
        return promo_type

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value is None or value <= 0:
            raise ValidationError("Value must be greater than 0.")
        return value

    def clean_min_payment(self):
        min_payment = self.cleaned_data.get('min_payment')
        if min_payment is None or min_payment <= 0:
            raise ValidationError("Minimum payment must be greater than 0.")
        return min_payment

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < date.today():
            raise ValidationError("Expiry date cannot be in the past.")
        return expiry_date

    # Validasi dan pastikan keunikan promo code
    def clean(self):
        cleaned_data = super().clean()
        
        # Minimal 1 restoran terpilih
        if not cleaned_data.get('restaurant'):
            raise ValidationError("Please select at least one restaurant for this promo.")
        
        # Promo code harus unik, exception case untuk edit kalau idnya sama
        promo_code = cleaned_data.get('promo_code')
        if promo_code and Promo.objects.filter(promo_code=promo_code).exclude(id=self.instance.id).exists():
            self.add_error('promo_code', "Promo code must be unique.")
        if promo_code and len(promo_code)>30:
            self.add_error('promo_code', "Promo code must be under 30 characters.")
        
        return cleaned_data
