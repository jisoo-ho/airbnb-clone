from django.core.management.base import BaseCommand
from rooms.models import Facility

# python manage.py seed_facilities : 사용 명령어(use in zsh terminal)
class Command(BaseCommand):

    help = "이 커맨드는 내부 시설을 생성합니다."

    def handle(self, *args, **options):
        facilities = [  # airbnb 내부 시설 발췌
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} 시설(퍼실리티) 생성 완료"))
