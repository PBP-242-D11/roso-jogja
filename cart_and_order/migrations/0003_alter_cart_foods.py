# Generated by Django 5.1.2 on 2024-10-24 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_order', '0002_alter_cart_foods'),
        ('restaurant', '0002_alter_restaurant_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='foods',
            field=models.ManyToManyField(blank=True, to='restaurant.food'),
        ),
    ]