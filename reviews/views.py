from django.shortcuts import redirect, reverse
from django.contrib import messages
from rooms import models as room_models
from . import forms


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            print("여기")
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
        else:
            messages.error(request, "Error!!")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
