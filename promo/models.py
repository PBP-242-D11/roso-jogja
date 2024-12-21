from django.db import models
from django.core.exceptions import ValidationError
import uuid
from datetime import date
from restaurant.models import Restaurant

class Promo(models.Model):
    TYPE_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Fixed Price', 'Fixed Price'),
    ]
    user = models.ForeignKey(
        "main.User",
        on_delete=models.CASCADE,
        related_name="promo",
        null=True,
        blank=True,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, null=False)
    value = models.FloatField(null=False)
    min_payment = models.FloatField(null=False)
    restaurant = models.ManyToManyField(Restaurant)
    promo_code = models.CharField(max_length=30, blank=True, null=True)
    expiry_date = models.DateField()
    max_usage = models.IntegerField(default=-1)
    shown_to_public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type} - {self.promo_code}'
    
    def use_promo(self, payment, restaurant_id):
        if self.expiry_date and (date.today() > self.expiry_date):
            return -3  # State: promo expired
        if not self.restaurant.filter(id=restaurant_id).exists():
            return -4  # State: invalid restaurant 
        if (payment<self.min_payment):
            return -1 # State: payment gacukup untuk pakai promo
        if (self.max_usage==0):
            return 0 # State: voucher habis
        else: # State: untuk voucher available
            if self.type == "Percentage":
                self.max_usage-=1
                return float(payment)*(100-self.value)/100 # State: promo yang dipakai persentase
            elif self.type == "Fixed Price":
                self.max_usage-=1
                return float(payment)-self.value # State: promo yang dipakai fixed price
        return -2 # Unknown error
    
    def simulate_promo(self, payment, restaurant_id):
        if self.expiry_date and (date.today() > self.expiry_date):
            return -3  # State: promo expired
        if not self.restaurant.filter(id=restaurant_id).exists():
            return -4  # State: invalid restaurant 
        if (payment<self.min_payment):
            return -1 # State: payment gacukup untuk pakai promo
        if (self.max_usage==0):
            return 0 # State: voucher habis
        else: # State: untuk voucher available
            if self.type == "Percentage":
                return float(payment)*(100-self.value)/100 # State: promo yang dipakai persentase
            elif self.type == "Fixed Price":
                return float(payment)-self.value # State: promo yang dipakai fixed price
        return -2 # Unknown error