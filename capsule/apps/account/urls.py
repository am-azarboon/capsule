from django.contrib.auth.views import LogoutView, PasswordResetCompleteView
from django.urls import path
from . import views


# urls base name
app_name = "account"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="account:login"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify"),
    path("resend-code/", views.ResendCodeView.as_view(), name="resend"),

    path("password-reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path("password-reset/confirm/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("password-reset/complete/", PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name="password-reset-complete"),
]
