from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """리뷰 어드민 정의"""

    list_display = ("__str__", "rating_average")
