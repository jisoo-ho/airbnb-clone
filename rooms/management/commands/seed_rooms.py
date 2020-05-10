import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

# python manage.py seed_rooms : 사용 명령어(use in zsh terminal)


class Command(BaseCommand):

    help = "이 커맨드는 방을 생성합니다."

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="몇 개의 방을 생성하시겠습니까")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()  # 모든 유저를 가져오기 때문에 DB가 클 경우 사용X
        room_types = room_models.RoomType.objects.all()  # 모든 룸 타입 호출
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),  # faker lib을 이용하여 가상 주소 생성
                "host": lambda x: random.choice(all_users),  # 랜덤 호스트 선택
                "room_type": lambda x: random.choice(room_types),  # 랜덤 룸타입 선택
                "guests": lambda x: random.randint(1, 20),  # 게스트, 가격 등 입력 숫자 범위 지정
                "price": lambda x: random.randint(40000, 100000),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))  # 리스트 추출
        for pk in created_clean:  # 생성된 모든 룸을
            room = room_models.Room.objects.get(pk=pk)  # pk로 방을 찾고 객체 생성
            for i in range(3, random.randint(10, 17)):  # 3부터 10|17 까지
                room_models.Photo.objects.create(  # 사진을 만들 때
                    caption=seeder.faker.sentence(),  # 가상의 설명과
                    file=f"/room_photos/{random.randint(1, 31)}.webp",  # 폴더 내부에 있는 파일
                    room=room,  # 을 선택된 방에 넣어준다.
                )
        self.stdout.write(self.style.SUCCESS(f"{number} 방 생성 완료"))
