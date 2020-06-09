from django.db import models
from . import managers

# Create your models here.
class TimeStampedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()
    # 데이터베이스에 추가 되지 않기 위해서 추상클래스
    class Meta:
        abstract = True
