from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

# python manage.py seed_users : 사용 명령어(use in zsh terminal)
class Command(BaseCommand):

    help = "이 커맨드는 다수의 유저를 생성합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="몇명의 유저를 생성하시겠습니까?",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} 유저 생성 완료"))
