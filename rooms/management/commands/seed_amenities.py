from django.core.management.base import BaseCommand
from rooms.models import Amenity

# python manage.py seed_amenities : 사용 명령어(use in zsh terminal)
class Command(BaseCommand):

    help = "이 커맨드는 어메니티를 생성합니다."

    def handle(self, *args, **options):
        amenities = [  # airbnb 홈페이지 내부의 어메니티 추출
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)  # create : CRUD 역할
        self.stdout.write(self.style.SUCCESS("어메니티 생성 완료"))
