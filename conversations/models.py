from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    """ 대화 클래스 정의 """

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    """ datetime 반환값을 str 로 변경 """

    def __str__(self):
        usernames = []
        for user in self.participants.all():  # 모드 유저 정보 전달
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampedModel):
    """ 메시지 클래스 정의 """

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says : {self.message}"
