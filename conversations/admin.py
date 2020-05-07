from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ 메시지 어드민 정의 """

    pass


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ 메시지 어드민 정의 """

    pass
