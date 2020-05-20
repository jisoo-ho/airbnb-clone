from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator  # 페이징
from . import models, forms

# home.html 파일명을 room_list.html로 변경(HomeView 요구사항 충족)
class HomeView(ListView):

    """ 홈 뷰 정의 """

    model = models.Room  # 전체 방 목록 호출
    paginate_by = 12  # 한 번에 보여줄 방 개수
    paginate_orphans = 5  # 5개 미만의 방이 페이지에 있다면 이전 페이지에서 출력
    ordering = "created"  # 생성순 정렬
    context_object_name = "rooms"


class RoomDetail(DetailView):
    # 장고는 DetailView를 사용하면 기본적으로 url argument로 pk를 찾는다.
    # urlpatterns = [path("<int:pk>", <- 이부분의 pk를 찾음

    """ 방 조회 정의 """

    model = models.Room


class SearchView(View):
    """ 검색 페이지 정의 """

    def get(self, request):

        country = request.GET.get("country")
        """country에 아무것도 없다면 (else) 빈 폼을 생성한다. 
        폼에 에러가 있다면 if문 밖에서 폼을 다시 렌더링 함.
        폼에 에러가 없다면 정상 작동.
        """
        if country:

            form = forms.SearchForm(request.GET)  # 검색한 내용을 기억하기 위한 request.GET

            if form.is_valid():  # form 에 에러가 없으면 True
                # cleaned_data로 정제된 데이터를 불러올 수 있다.(from forms.py)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True
                # pk로 필터링 할 필요 없음
                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                # 페이징 처리
                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:

            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})

