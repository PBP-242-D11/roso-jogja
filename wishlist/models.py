from django.db import models

from main.models import User
from restaurant.models import Restaurant

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user.username}'s wishlist"
