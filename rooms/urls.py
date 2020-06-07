from django.urls import path
from rooms import views as rooms_views

app_name = "rooms"

urlpatterns = [
    path("create/", rooms_views.UploadRoomView.as_view(), name="create"),
    path("<int:pk>/", rooms_views.RoomDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", rooms_views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", rooms_views.RoomPhotosView.as_view(), name="edit_photos"),
    path("<int:pk>/photos/add", rooms_views.AddPhotoView.as_view(), name="add_photo"),
    path(
        "<int:room_pk>/photos/<int:photos_pk>/delete/",
        rooms_views.delete_photo,
        name="delete_photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photos_pk>/update/",
        rooms_views.EditPhotoView.as_view(),
        name="update_photo",
    ),
    path("search/", rooms_views.SearchView.as_view(), name="search"),
]
