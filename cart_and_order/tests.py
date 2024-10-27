import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Cart, Order, OrderItem
from restaurant.models import Food, Restaurant
from decimal import Decimal

User = get_user_model()

class CartAndOrderTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.food = Food.objects.create(name="Burger", price=50, restaurant=self.restaurant)
        self.cart = Cart.objects.create(user=self.user, restaurant=self.restaurant)

    def tearDown(self):
        self.cart.cart_items.all().delete()
        self.cart.restaurant = None
        self.cart.save()

    # Test total price calculation in order
    def test_calculate_total_price_in_order(self):
        self.order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            payment_method="CREDIT",
            total_price=0
        )
        OrderItem.objects.create(order=self.order, food=self.food, quantity=2, price_at_order=self.food.price)
        self.assertEqual(self.order.calculate_total_price, Decimal(100))  

    # Test if total_price is set correctly on save
    def test_order_total_price_on_save(self):
        self.order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            payment_method="CREDIT",
            total_price=0
        )
        OrderItem.objects.create(order=self.order, food=self.food, quantity=2, price_at_order=self.food.price)
        self.order.save()
        self.assertEqual(self.order.total_price, Decimal(100))

    # Test creating order
    def test_create_order_view(self):
        self.cart.add_food(self.food, quantity=2)
        url = reverse('order:create_order')
        response = self.client.post(
            url,
            json.dumps({
                "payment_method": "CREDIT",
                "final_price": 100,
                "notes": "Please deliver quickly"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Order.objects.filter(user=self.user).exists())

    # Test clearing the cart
    def test_clear_cart_view(self):
        url = reverse('order:clear_cart')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.cart.cart_items.exists())

    # Test Menampilkan Riwayat Pesanan
    def test_show_orders_view(self):
        order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            payment_method="CREDIT",
            total_price=100
        )
        url = reverse('order:show_order_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.restaurant.name)
        self.assertContains(response, "Order History")