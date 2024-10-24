import uuid
from django.db import models
from restaurant.models import Food, Restaurant
from django.db.models import Sum

class Cart(models.Model):
    user = models.OneToOneField("main.User", on_delete=models.CASCADE, primary_key=True)
    foods = models.ManyToManyField(Food, blank=True)
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

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('CREDIT', 'Credit Card'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Cash on Delivery'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey("main.User", on_delete=models.CASCADE)
    foods = models.ManyToManyField(Food)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    notes = models.TextField(null = True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.first_name}"

