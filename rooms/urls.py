from django.urls import path
from rooms import views as rooms_views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", rooms_views.RoomDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", rooms_views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", rooms_views.RoomPhotosView.as_view(), name="edit_photos"),
    path("search/", rooms_views.SearchView.as_view(), name="search"),
]
