from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from rooms import models as rooms_models


class HomeView(ListView):

    """"HomeView Definition as ListView """

    model = rooms_models.Room
    paginate_by = 10
    context_object_name = "rooms"
    template_name = "rooms/rooms_list.html"


# DetailView functional
#
#
# def detail(request, pk):
#     try:
#         room_detail = rooms_models.Room.objects.get(pk=pk)
#         return render(
#             request, "rooms/detail.html", context={"room_detail": room_detail},
#         )
#     except rooms_models.Room.DoesNotExist:
#         raise Http404()


class DetailView(DetailView):

    """ DetailView Definition as DetailView """

    model = rooms_models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    s_country = request.GET.get("country", "KR")
    s_room_types = int(request.GET.get("room_type", 0))
    room_types = rooms_models.RoomType.objects.all()

    form = {
        "city": city,
        "s_country": s_country,
        "s_room_types": s_room_types,
    }

    choices = {"countries": countries, "room_types": room_types}
    return render(request, "rooms/search.html", context={**form, **choices},)
