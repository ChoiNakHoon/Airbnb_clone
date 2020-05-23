from django.views.generic import ListView
from django.shortcuts import render
from rooms import models as rooms_models


class HomeView(ListView):

    """"HomeView Definition as ListView """

    model = rooms_models.Room
    paginate_by = 10
    context_object_name = "rooms"
    template_name = "rooms/rooms_list.html"


def detail(request, pk):
    print(pk)
    room_detail = rooms_models.Room.objects.get(pk=pk)
    print(vars(room_detail.amenities.all))
    return render(request, "rooms/detail.html", context={"room_detail": room_detail},)
