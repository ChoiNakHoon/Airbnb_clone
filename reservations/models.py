import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDays(core_models.TimeStampedModel):

    """ BookedDay Model Definition """

    day = models.DateField(blank=True)
    reservation = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"


# 예약하면 check_in과 check out이 기록 된다.
# 하지만 그 사이의 값은 어떤 변경 사항을 가지는 지 알 수가 없다
# 그래서 booking day model을 생성하여 reservation save일 때
# check_in에서 check_out 까지 범위를 booking day에 기록한 다음
# 그 object를 이용해서 예약 상태를 view(html)에 나타낸다.
class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confiremd"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confiremd"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{0} - {1}".format(self.room, self.check_in)

    def is_progress(self):
        now = timezone.now().date()
        return now < self.check_out and self.check_in <= now

    is_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    # save 할때마다 booked Day에 save 하면 안 되니깐 intercept
    # 이미 reservation이 있다면 (pk) 저장 안 하고 새로운 reservation에 추가
    def save(self, *args, **kwargs):
        # 만약 pk가 None 라면 새로운 reservation
        if self.pk is None:
            # new reservation
            start = self.check_in
            end = self.check_out
            difference = end - start
            # 방(room)마다 예약된 날짜를 range로 찾아서 존재여부 확인 (기준 : check_in ~ check_out)
            existing_booked_day = BookedDays.objects.filter(
                day__range=(start, end), reservation__room=self.room
            ).exists()
            # 존재 하지 않는 다면
            if not existing_booked_day:
                # 저장 한다.
                super().save(*args, **kwargs)
                # difference가 6이면 7일로 만들어 줌
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDays.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)  # Call the real save() method
