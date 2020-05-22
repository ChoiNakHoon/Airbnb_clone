from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):
    help = "This command created amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",
    #         help="How many times do you want me to tell you that I  love you?",
    #     )

    def handle(self, *args, **options):

        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Washer",
            "Dryer",
            "Wifi",
            "Breakfast",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Laptop-friendly workspace",
            "TV",
            "Crib",
            "High chair",
            "Self check-in",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Private bathroom",
        ]

        for item in amenities:
            Amenity.objects.create(name=item)

        self.stdout.write(self.style.SUCCESS("Amenities Created"))
        # times = options.get("times")
        # for i in range(0, int(times)):
        #     self.stdout.write(self.style.NOTICE("i love you"))
