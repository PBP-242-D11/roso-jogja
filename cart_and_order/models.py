import uuid
from django.db import models
from restaurant.models import Food, Restaurant
from django.db.models import Sum

class Cart(models.Model):
    user = models.OneToOneField("main.User", on_delete=models.CASCADE, primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.user.first_name}"

    @property
    def total_price(self):
        return sum(cart_item.price for cart_item in self.cart_items.all())

    @property
    def total_item(self):
        return sum(cart_item.quantity for cart_item in self.cart_items.all())
        
    def add_food(self, food, quantity=1):
        # Set restaurant if not yet set
        if not self.restaurant:
            self.restaurant = food.restaurant
            self.save()

        # Ensure food is from the same restaurant
        if food.restaurant == self.restaurant:
            cart_item, created = CartItem.objects.get_or_create(cart=self, food=food)
            cart_item.quantity += quantity if not created else quantity
            cart_item.save()
        else:
            raise ValueError("All foods in the cart must be from the same restaurant.")

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def price(self):
        return self.food.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.food.name}"

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('CREDIT', 'Credit Card'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Cash on Delivery'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey("main.User", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    promo_cut = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.first_name}"

    @property
    def calculate_total_price(self):
        # Use F() expression to multiply price_at_order with quantity
        from django.db.models import F
        total = self.order_items.aggregate(
            total=Sum(F('price_at_order') * F('quantity'))
        )['total'] or 0
        return total

    def save(self, *args, **kwargs):
        # Ensure the order has a primary key before calculating total price
        if not self.pk:
            super(Order, self).save(*args, **kwargs)  # Save to generate primary key
        if self.total_price == 0:
            self.total_price = self.calculate_total_price  # Calculate total price
        self.promo_cut = self.calculate_total_price - self.total_price
        super(Order, self).save(update_fields=['total_price'])  # Save with updated total_price

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.food.name} in order {self.order.order_id}"

    def save(self, *args, **kwargs):
        # Set price_at_order to current food price if not already set
        if not self.price_at_order:
            self.price_at_order = self.food.price
        super().save(*args, **kwargs)

