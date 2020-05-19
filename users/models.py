import uuid  # 랜덤한 값을 생성할 모듈
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail  # 이메일 전송 모듈
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):

    """커스텀 유저 모델 """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGING_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGING_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)  # 이메일 확인
    email_secret = models.CharField(max_length=20, default="", blank=True)  # 이메일 인증 키
    # 이메일과 비밀번호를 이용해서 새 계정을 생성하면 email_secret 에 인증키가 생성 된다.
    # 그리고 해당 이메일로 인증키를 보낸다. 해당 키가 일치하면 인증 완료

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(  # String을 렌더링
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Airbnb 계정을 인증합니다.",
                strip_tags(html_message),  # html을 태그형태를 제외하여 반환
                settings.EMAIL_FROM,  # 보낸이
                [self.email],  # 받는이(여러명 설정 가능)
                fail_silently=False,  # 에러가 발생한 경우 에러로 표시
                html_message=html_message,
            )
            self.save()  # 유저 저장
        return
