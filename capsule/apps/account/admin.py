from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.contrib import admin

from .models import User, PasswordResetToken


# Unregister Group
admin.site.unregister(Group)


# User ModelAdmin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "mobile", "full_name", "verify", "is_active"]
    list_display_links = ["username"]
    list_filter = ["is_staff", "verify", "is_active"]

    fieldsets = [
        (None, {"fields": ("username",)}),
        (_("Personal info"), {"fields": ("full_name", "mobile", "melli", "date_of_birth")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    ]


admin.site.register(PasswordResetToken)
