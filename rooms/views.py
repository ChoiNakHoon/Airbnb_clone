from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_countries import countries
from django.urls import reverse_lazy
from rooms import models as rooms_models
from users import mixins as user_mixins
from . import forms


class HomeView(ListView):

    """"HomeView Definition as ListView """

    model = rooms_models.Room
    paginate_by = 12
    paginate_orphans = 5
    context_object_name = "rooms"
    template_name = "rooms/rooms_list.html"


class RoomDetailView(DetailView):

    """ DetailView Definition as DetailView """

    model = rooms_models.Room


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):
        form = forms.SearchForm(request.GET)

        if form.is_valid():

            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            beds = form.cleaned_data.get("beds")
            bedrooms = form.cleaned_data.get("bedrooms")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            # # filter
            filter_args = {}

            # city가 Anywhere가 아니라면
            if city != "Anywhere":
                # filter_args에 filter할 key(city)와 옵션을 기입
                filter_args["city__startswith"] = city

            # 이하 비슷한 방법으로 코딩 하거나 default 값이 없는 경우는 keyword만
            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            # gte : 같거나 큼
            # lte : 같거나 작음
            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if beds is not None:
                filter_args["beds__gte"] = beds

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True
            # filter keyword로 필터링

            if amenities is not None:
                for amenity in amenities:
                    filter_args["amenities"] = amenity

            if facilities is not None:
                for facility in facilities:
                    filter_args["facilities"] = facility

            queryset = rooms_models.Room.objects.filter(**filter_args).order_by(
                "-created"
            )

            paginator = Paginator(queryset, 3, orphans=1)

            page = request.GET.get("page", 1)

            rooms = paginator.get_page(page)

            get_copy = request.GET.copy()
            address = get_copy.pop("page", True) and get_copy.urlencode()

            return render(
                request,
                "rooms/search.html",
                context={"form": form, "rooms": rooms, "address": address},
            )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", context={"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    """ Room Update Definition """

    model = rooms_models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rule",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    """ RoomPhotos View Definition """

    model = rooms_models.Room
    template_name = "rooms/room_photos.html"
    # Room을 생성한 유저가 맞다면 Room의 Photo를 가져 온다.
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photos_pk):
    user = request.user
    try:
        room = rooms_models.Room.objects.get(pk=room_pk)
        # room.pk와 현재 로그인 중인 유저 pk가 같지 않다면
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            rooms_models.Photo.objects.filter(pk=photos_pk).delete()
            messages.info(request, "Photo Deleted!")
        return redirect(reverse("rooms:edit_photos", kwargs={"pk": room_pk}))
    except rooms_models.Room.DoesNotExists:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = rooms_models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photos_pk"
    fields = ("caption",)
    success_message = "Photo Updated."

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:edit_photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):

    model = rooms_models.Photo
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm
    fields = (
        "caption",
        "file",
    )

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.info(self.request, "Photo Created!")
        return redirect(reverse("rooms:edit_photos", kwargs={"pk": pk}))
