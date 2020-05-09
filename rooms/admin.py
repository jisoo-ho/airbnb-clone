from django.contrib import admin
from . import models
from django.utils.html import mark_safe


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ 아이템 어드민 정의 """

    list_display = ("name", "used_by")

    def used_by(self, object):
        return object.rooms.count()


class PhotoInline(admin.TabularInline):  # StackedInline도 사용 가능(직렬정렬)
    """사진과 방을 연결(파일과 설명만으로 방과 연결시키기 위함)"""

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """룸 어드민 정의"""

    inlines = (PhotoInline,)  # 사진, 방 연결 클래스 호출

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")},),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)},),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = ("=city", "^host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    """def save_model(self, request, obj, form, change):
        #어드민 패널 컨트롤
        print(obj, change, form)
        super().save_model(request, obj, form, change)"""

    # self는 RoomAdmin, object는 Rooms의 현재 행
    def count_amenities(self, object):
        return object.amenities.count()

    def count_photos(self, object):
        return object.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ 사진 어드민 정의 """

    list_display = ("__str__", "get_thumbnail")

    """썸네일 출력하기"""

    def get_thumbnail(self, object):
        # print(object.file.path)
        """print(
            type(object.file)
        )"""  # <class 'django.db.models.fields.files.ImageFieldFile'>
        return mark_safe(f'<img width="50px" src="{object.file.url}" />')
        # html사용 가능 함수 mark_safe

    get_thumbnail.short_description = "Thumbnail"
