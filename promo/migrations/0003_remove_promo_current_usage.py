# Generated by Django 5.1.2 on 2024-10-24 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0002_remove_promo_restaurant_promo_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promo',
            name='current_usage',
        ),
    ]
