import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "리스트"


class Command(BaseCommand):

    help = f"이 커맨드는 {NAME}를 생성합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help=f"몇 개의 {NAME}를 생성하시겠습니까"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users),},
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)  # *은 array내부의 요소를 추출 시 사용

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} 생성 완료"))
