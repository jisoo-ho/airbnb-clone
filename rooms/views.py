from math import ceil
from django.shortcuts import render  # HTML 태그를 이용 가능하게 함
from . import models

# from django.http import HttpResponse  # HttpResponse 객체 반환하기 위한 import

# 페이지 네비게이터
def all_rooms(request):
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )
    # context 이름은 전달받는 html 파일의 변수명과 같아야 한다.
