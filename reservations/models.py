from django.db import models
from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """예약 정의"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRM = "confirmed"
    STATUS_CALCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "pending"),
        (STATUS_CONFIRM, "confirmed"),
        (STATUS_CALCELED, "canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room} - {self.check_in}"

