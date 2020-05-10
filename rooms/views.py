from django.views.generic import ListView
from . import models

# home.html 파일명을 room_list.html로 변경(HomeView 요구사항 충족)
class HomeView(ListView):

    """ 홈 뷰 정의 """

    model = models.Room  # 전체 방 목록 호출
    paginate_by = 10  # 한 번에 보여줄 방 개수
    paginate_orphans = 5  # 5개 미만의 방이 페이지에 있다면 이전 페이지에서 출력
    ordering = "created"  # 생성순 정렬
    context_object_name = "rooms"
