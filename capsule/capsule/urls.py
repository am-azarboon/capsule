from django.contrib import admin
from django.urls import path, include


# Base urls
urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("apps.account.urls", namespace="account")),
]
