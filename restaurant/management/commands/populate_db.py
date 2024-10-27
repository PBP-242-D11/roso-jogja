import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from restaurant.models import Food, Restaurant


class Command(BaseCommand):

    help = "Populate the database with some initial data"

    def handle(self, *args, **options):
        dir = os.path.join(
            settings.BASE_DIR,
            "restaurant",
            "management",
            "commands",
            "foods_combined.json",
        )

        # Get json data
        with open(dir, "r") as f:
            data = json.load(f)

        Restaurant.objects.all().delete()
        Food.objects.all().delete()

        # Create restaurants
        for resto_name, resto in data.items():
            self.stdout.write(self.style.SUCCESS(f"Creating restaurant: {resto_name}"))
            r = Restaurant.objects.create(
                name=resto_name,
                address=resto.get("address", ""),
                categories=resto.get("category", ""),
                description="",
            )

            foods = resto["foods"]
            for food in foods:
                try:
                    desc = food.get("desc", None)
                    price = food.get("price", None)
                    if price is None:
                        price = "0"
                    if desc is None:
                        desc = ""
                    Food.objects.create(
                        name=food["name"],
                        description=desc,
                        price=price.replace(".", ""),
                        restaurant=r,
                    )
                except:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to create food: {food['name']}")
                    )

        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))
