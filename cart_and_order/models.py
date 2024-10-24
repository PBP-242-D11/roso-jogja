import uuid
from django.db import models
from restaurant.models import Food, Restaurant
from main.models import User
from django.db.models import Sum

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    foods = models.ManyToManyField(Food, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.user.first_name}"

    def total_price(self):
        return self.foods.aggregate(total=Sum('price'))['total'] or 0

    def add_food(self, food):
        if not self.restaurant:
            self.restaurant = food.restaurant
            self.save()
        
        if food.restaurant == self.restaurant:
            self.foods.add(food)
        else:
            raise ValueError("All foods in the cart must be from the same restaurant.")
