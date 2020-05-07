from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    """ 대화 클래스 정의 """

    participants = models.ManyToManyField("users.User", blank=True)

    """ datetime 반환값을 str 로 변경 """

    def __str__(self):
        return str(self.created)


class Message(core_models.TimeStampedModel):
    """ 메시지 클래스 정의 """

    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} says : {self.text}"
