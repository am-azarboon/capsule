from django.urls import path
from . import views


# urls base name
app_name = "console"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("passwords/", views.PasswordsView.as_view(), name="passwords"),
    path("cards/", views.CardsView.as_view(), name="cards"),

    path("archives/", views.ArchivesView.as_view(), name="archives"),
    path("archive/<int:pk>/", views.AddToArchiveView.as_view(), name="add-archive"),

    path("add-pass/", views.AddPasswordView.as_view(), name="add-pass"),
    path("edit-pass/<int:pk>/", views.EditPasswordView.as_view(), name="edit-pass"),
    path("del-pass/<int:pk>/", views.DeletePasswordView.as_view(), name="del-pass"),

    path("add-card/", views.AddCardView.as_view(), name="add-card"),
    path("edit-card/<int:pk>/", views.EditCardView.as_view(), name="edit-card"),
    path("del-card/<int:pk>/", views.DeleteCardView.as_view(), name="del-card"),
]
