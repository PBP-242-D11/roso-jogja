from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from main.models import User
from promo.models import Promo
from cart_and_order.models import Cart, Order
from restaurant.models import Restaurant
from datetime import timedelta

class PromoFeatureTests(TestCase):
    
    def setUp(self):
        self.customer = User.objects.create_user(username="customer", password="RosoJogja", role="C")
        self.owner = User.objects.create_user(username="owner", password="RosoJogja", role="R")
        self.admin = User.objects.create_superuser(username="admin", password="RosoJogja", role="A")

        self.visible_promo = Promo.objects.create(
            promo_code="VISIBLEPROMO", min_payment=100, max_usage=10, shown_to_public=True,
            value=10, type="Percentage", expiry_date=timezone.now().date() + timedelta(days=5)
        )
        self.hidden_promo = Promo.objects.create(
            promo_code="HIDDENPROMO", min_payment=200, max_usage=5, shown_to_public=False,
            value=10, type="Fixed Price", expiry_date=timezone.now().date() + timedelta(days=5)
        )
        self.restaurant = Restaurant.objects.create(name="resto",address="alamat resto",price_range=1000,description="deskripsi resto",owner=self.owner)

    def test_admin_access_all_promos(self):
        self.client.login(username="admin", password="RosoJogja")
        response = self.client.get('/promo/')
        
        self.assertContains(response, "10.0% Off")
        self.assertContains(response, "Rp10")

    def test_customer_access_visible_promos(self):
        self.client.login(username="customer", password="RosoJogja")
        response = self.client.get('/promo/')
        
        self.assertContains(response, "10.0% Off")
        self.assertNotContains(response, "Rp10 Off")

    def test_owner_access_promos(self):
        self.client.login(username="owner", password="RosoJogja")
        response = self.client.get('/promo/')
        
        self.assertContains(response, "10.0% Off")
        self.assertContains(response, "Rp10")
