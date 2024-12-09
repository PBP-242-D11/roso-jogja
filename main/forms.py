from django import forms
from django.contrib.auth.forms import UserCreationForm

from main.models import User


class CustomRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "role",
            "phone_number",
            "address",
            "profile_picture",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if address and len(address) < 10:
            raise forms.ValidationError("Address must be at least 10 characters long.")
        return address
