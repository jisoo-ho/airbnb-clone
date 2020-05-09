from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    """ 리스트 어드민 정의 """

    list_display = ("name", "user", "count_rooms")
    search_fields = ("name",)
    filter_horizontal = ("rooms",)
