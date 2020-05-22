from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "This command created facilities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",
    #         help="How many times do you want me to tell you that I  love you?",
    #     )

    def handle(self, *args, **options):
        facilities = [
            "Free parking on premises",
            "Gym",
            "Hot tub",
            "Pool",
        ]

        for item in facilities:
            Facility.objects.create(name=item)

        self.stdout.write(
            self.style.SUCCESS("{} Facilities Created".format(len(facilities)))
        )
        # times = options.get("times")
        # for i in range(0, int(times)):
        #     self.stdout.write(self.style.NOTICE("i love you"))
