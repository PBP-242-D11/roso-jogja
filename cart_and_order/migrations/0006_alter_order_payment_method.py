# Generated by Django 5.1.2 on 2024-10-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_order', '0005_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('CREDIT', 'Credit Card'), ('PAYPAL', 'PayPal'), ('CASH', 'Cash on Delivery')], max_length=10),
        ),
    ]