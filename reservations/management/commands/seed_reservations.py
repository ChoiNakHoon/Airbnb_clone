import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as models_reservation
from users import models as models_user
from rooms import models as models_room

NAME = "Reservations"


class Command(BaseCommand):
    help = f"This command created many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = models_user.User.objects.all()
        rooms = models_room.Room.objects.all()
        seeder.add_entity(
            models_reservation.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confiremd", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
