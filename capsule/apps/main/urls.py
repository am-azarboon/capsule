from django.urls import path
from . import views


# urls base name
app_name = "main"

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
]
