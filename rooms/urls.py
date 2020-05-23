from django.urls import path
from rooms import views as rooms_views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", rooms_views.detail, name="detail"),
]
