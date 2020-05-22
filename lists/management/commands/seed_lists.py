import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as models_lists
from users import models as models_user
from rooms import models as models_room

NAME = "Lists"


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
            models_lists.List, number, {"user": lambda x: random.choice(users),},
        )
        created = seeder.execute()
        created_clean = flatten(list(created.values()))

        for pk in created_clean:
            list_model = models_lists.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
