# Generated by Django 5.1.2 on 2024-10-24 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_order', '0003_alter_cart_foods'),
        ('restaurant', '0002_alter_restaurant_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='foods',
        ),
        migrations.RemoveField(
            model_name='order',
            name='foods',
        ),
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart_and_order.cart')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.food')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price_at_order', models.DecimalField(decimal_places=2, max_digits=10)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='cart_and_order.order')),
            ],
        ),
    ]
