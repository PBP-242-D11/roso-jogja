# Generated by Django 5.1.2 on 2024-10-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0001_initial'),
        ('restaurant', '0002_alter_restaurant_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promo',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='promo',
            name='restaurant',
            field=models.ManyToManyField(to='restaurant.restaurant'),
        ),
    ]
