from django.db import models


class TimeStampedModel(models.Model):
    """ 타임 스탬프 모델 """

    """모델 저장 시 시간 자동 생성"""
    created = models.DateTimeField(auto_now_add=True)  # 모델이 생생성된 날짜
    updated = models.DateTimeField(auto_now=True)  # 새로운 날짜로 업데이트

    class Meta:
        abstract = True  # DB저장 방지
