from django.urls import path
from rooms import views as room_views

app_name = "core"
# HomeView class가 가진 as_view()함수 호출
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
