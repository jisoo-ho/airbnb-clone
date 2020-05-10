from django.urls import path
from rooms import views as room_views

app_name = "core"
# room_views.all_rooms : rooms>views.py 의 함수명과 같아야 한다.
urlpatterns = [path("", room_views.all_rooms, name="home")]
