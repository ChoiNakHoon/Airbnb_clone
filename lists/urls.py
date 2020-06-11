from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("add/<int:room_pk>/", views.toggle_room, name="toggle_room"),
    path("favs/", views.FavListView.as_view(), name="see_favs"),
]
