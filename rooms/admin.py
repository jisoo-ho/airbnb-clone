from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ 아이템 어드민 정의 """

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """룸 어드민 정의"""

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ 사진 어드민 정의 """

    pass
