from django.utils.translation import gettext as _
from django.conf.urls.static import static
from apps.account.views import LoginView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


# Base urls
urlpatterns = [
    path("admin/login/", LoginView.as_view()),
    path("admin/", admin.site.urls),
    path("account/", include("apps.account.urls", namespace="account")),
    path("", include("apps.main.urls", namespace="main")),
    path("dashboard/", include("apps.console.urls", namespace="console")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Rename site header & title & index_title
admin.site.site_header = _("Site Management")
admin.site.index_title = _("Management Panel")
admin.site.site_title = _("Capsule")
