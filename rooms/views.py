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
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    super_host = bool(request.GET.get("super_host", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_country": s_country,
        "s_room_types": s_room_types,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "instant": instant,
        "super_host": super_host,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }

    room_types = rooms_models.RoomType.objects.all()
    amenities = rooms_models.Amenity.objects.all()
    facilities = rooms_models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # filter
    filter_args = {}

    # city가 Anywhere가 아니라면
    if city != "Anywhere":
        # filter_args에 filter할 key(city)와 옵션을 기입
        filter_args["city__startswith"] = city

    # 이하 비슷한 방법으로 코딩 하거나 default 값이 없는 경우는 keyword만
    filter_args["country"] = s_country

    if s_room_types != 0:
        filter_args["room_type__pk"] = s_room_types

    # gte : 같거나 큼
    # lte : 같거나 작음
    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if super_host is True:
        filter_args["host__superhost"] = True
    # filter keyword로 필터링

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = rooms_models.Room.objects.filter(**filter_args)
    return render(
        request, "rooms/search.html", context={**form, **choices, "rooms": rooms},
    )
