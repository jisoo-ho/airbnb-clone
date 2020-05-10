from django.shortcuts import render, redirect  # HTML 태그를 이용 가능하게 함
from django.core.paginator import Paginator, EmptyPage
from . import models

# from django.http import HttpResponse  # HttpResponse 객체 반환하기 위한 import

# 페이지 네비게이터
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    # orphans는 5개 미만의 데이터가 페이지에 남는 경우 이전 페이지에서 한 번에 출력
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")

