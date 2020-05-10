from django.shortcuts import render  # HTML 태그를 이용 가능하게 함
from . import models

# from django.http import HttpResponse  # HttpResponse 객체 반환하기 위한 import


def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
    # context 이름은 전달받는 html 파일의 변수명과 같아야 한다.
