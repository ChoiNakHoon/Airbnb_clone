from django.contrib.auth.models import AbstractUser
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
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)

    superhost = models.BooleanField(default="False")
