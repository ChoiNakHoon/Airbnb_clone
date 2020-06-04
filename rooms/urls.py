from django.urls import path
from rooms import views as rooms_views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", rooms_views.DetailView.as_view(), name="detail"),
    path("search/", rooms_views.SearchView.as_view(), name="search"),
]
