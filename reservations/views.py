import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as reviews_forms
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
    def get(self, *args, **kwargs):

        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = reviews_forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            context={"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    # host가 reservation 관하여 수락 및 취소 선택 했을 때
    # 처리하여 유저에게 상태를 보여주는 역할
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDays.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
