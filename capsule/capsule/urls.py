from django.utils.translation import gettext as _
from apps.account.views import LoginView
from django.contrib import admin
from django.urls import path, include


# Base urls
urlpatterns = [
    path("admin/login/", LoginView.as_view()),
    path("admin/", admin.site.urls),
    path("account/", include("apps.account.urls", namespace="account")),
    path("", include("apps.main.urls", namespace="main")),
]


# Rename site header & title & index_title
admin.site.site_header = _("Site Management")
admin.site.index_title = _("Management Panel")
admin.site.site_title = _("Capsule")
