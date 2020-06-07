import datetime
from django import template
from reservations import models as reservations_models

register = template.Library()


@register.simple_tag
def is_booked(room, day):

    if day.number == 0:
        return
    try:
        # cal.py에서 가져온 데이터를 date type으로 변환해서 저장
        # 안 그럼 bookedDay에 있는 date type을 찾을 수 없음
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        # BookedDays 테이블에서 예약된 날짜와 예약한 룸을 찾는다.
        reservations_models.BookedDays.objects.get(day=date, reservation__room=room)
        return True
    except reservations_models.BookedDays.DoesNotExist:
        return False
