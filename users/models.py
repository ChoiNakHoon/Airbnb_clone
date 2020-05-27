import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db import models

# Create your models here.
# 필드 추가 할 때마다 default 값이 필요하다.
# 이전에 row에서는 새로 추가되는 column에 대한 row의 값이 없음
# default 값은 넣거나 혹은 NULL=TRUE 설정해서 값을 알려주고 migrations
class User(AbstractUser):
    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_KOREAN = "ko"
    LANGUAGE_ENGLISH = "en"
    LANGUAGE_SPANISH = "es"
    LANGUAGE_CHINESE = "zh"
    LANGUAGE_JAPNESE = "jp"

    LANGUAGE_CHOICES = (
        (LANGUAGE_KOREAN, "Korean"),
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_SPANISH, "Español"),
        (LANGUAGE_CHINESE, "汉语·中文"),
        (LANGUAGE_JAPNESE, "日本語"),
    )

    CURRENCY_KRW = "krw"
    CURRENCY_USD = "usd"
    CURRENCY_EUR = "eur"
    CURRENCY_CNY = "cny"
    CURRENCY_JPY = "jpy"

    CURRENCY_CHOICES = (
        (CURRENCY_KRW, "KRW"),
        (CURRENCY_USD, "USD"),
        (CURRENCY_EUR, "EUR"),
        (CURRENCY_CNY, "CNY"),
        (CURRENCY_JPY, "JPY"),
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
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    # 메일 인증 하기 위한 메소드
    # uuid로 key값을 생성하여 secret 변수에 넣음
    def verify_email(self):
        print("here")
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            # email_secret에 secret 값을 넣음
            self.email_secret = secret
            # 그리고 sendmail로 인증 메일을 보냄.
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret,}
            )
            send_mail(
                "Verify Airbnb Account",  # 제목
                strip_tags(html_message),  # 인증 링크
                settings.EMAIL_FROM,  # 보내는 이메일 주소
                [self.email],  # 받는 이메일 주소
                fail_silently=False,  # 에러 여부
                html_message=html_message,
            )
            self.save()
        return
