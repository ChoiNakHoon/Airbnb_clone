from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render
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
