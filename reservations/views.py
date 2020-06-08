import datetime
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from . import models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):

    try:
        # BookDays db에 존재 한다면
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDays.objects.get(day=date_obj, reservation__room=room)
        # 만들수가 없죠
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        # 룸이 없다면 역시 못 만들구요
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDays.DoesNotExist:
        # 존재 하지 않으면 예약합니다.
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        messages.info(request, "Reservation completed")
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, pk):
        try:
            reservation = models.Reservation.objects.get(pk=pk)
        except models.Reservation.DoesNotExists:
            pass
