from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from users import models as users_models
from rooms import models as rooms_models
from . import models as lists_models


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = rooms_models.Room.objects.get_or_none(pk=room_pk)

    if room is not None and action is not None:
        # unppacking list
        the_list, _ = lists_models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
            room.likes.add(request.user)
        elif action == "remove":
            the_list.rooms.remove(room)
            room.likes.remove(request.user)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class FavListView(TemplateView):

    """ SeeFav View Definition """

    template_name = "lists/list.html"
