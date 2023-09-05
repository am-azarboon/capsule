from django.utils.translation import gettext as _
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import FormView, View
from django.contrib.auth import login
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from .mixins import LogoutRequiredMixin, VerifyPreviousUrlMixin
from .handlers import CreateEmailMessage, SendEmailThread
from .models import User, PasswordResetToken
from . import forms
import json


# Render Login view
class LoginView(LogoutRequiredMixin, FormView):
    template_name = "account/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("account:main")

    def get_success_url(self):
        """ Change success url based on 'next' parameter """
        next_url = self.request.GET.get("next")
        return next_url if next_url else super().get_success_url()

    def form_valid(self, form):
        """ Get authenticated user and login """
        user = form.cleaned_data.get("user")
        login(self.request, user)
        return super().form_valid(form)


# Render Register View
class RegisterView(LogoutRequiredMixin, FormView):
    template_name = "account/register.html"
    form_class = forms.RegisterForm
    success_url = reverse_lazy("account:verify")

    def dispatch(self, request, *args, **kwargs):
        """ Do something before generating form class (here is flush sessions) """
        self.request.session.flush()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ Get created user and redirect to email verification page """
        user = form.cleaned_data.get("user")

        # Create new verification message
        email = CreateEmailMessage(verification=True)
        email.email_verify_message()

        # Send email by async thread
        email_t = SendEmailThread(user.username, email.subject, email.message)
        email_t.start()

        # Save user_id and verification code in sessions
        self.request.session["user_id"] = user.pk
        self.request.session["code"] = email.code
        self.request.session.set_expiry(0)

        return super().form_valid(form)


# Render VerifyEmail View
class VerifyEmailView(LogoutRequiredMixin, VerifyPreviousUrlMixin, FormView):
    template_name = "account/verification.html"
    form_class = forms.EmailVerifyForm
    success_url = reverse_lazy("account:main")

    def get_success_url(self):
        """ Change success url based on ?next parameter """
        next_url = self.request.GET.get("next")
        return next_url if next_url else super().get_success_url()

    def form_valid(self, form):
        """ Get user & sent code in sessions and compare them. then login user """
        session = self.request.session

        user_code = form.cleaned_data.get("code")
        code = session.get("code")

        if not code:
            form.add_error("code", _("Code has bean expired! Please try again."))
            return super().form_invalid(form)  # Return invalid form
        elif code != user_code:
            form.add_error("code", _("Entered code is not correct!"))
            return super().form_invalid(form)  # Return invalid form

        # Try to get user and login
        try:
            user = User.objects.get(pk=session.get("user_id"))
            if not user.verify:
                user.verify = True
                user.save()
        except User.DoesNotExist:
            form.add_error("code", _("Code has bean expired! Please try again."))
            return super().form_invalid(form)

        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        # Delete code from sessions
        if "code" in session:
            del session["code"]

        return super().form_valid(form)


# Resend VerifyCode View
class ResendCodeView(LogoutRequiredMixin, View):
    def post(self, request):
        response = json.loads(request.body)
        send_value = response.get("send")

        if send_value and "user_id" in request.session:
            try:
                user = User.objects.get(pk=request.session["user_id"])
            except User.DoesNotExist:
                return JsonResponse({"status": 403})

            # Create new verification message
            email = CreateEmailMessage(verification=True)
            email.email_verify_message()

            # Send email by async thread
            email_t = SendEmailThread(user.username, email.subject, email.message)
            email_t.start()

            # Save user_id and verification code in sessions
            request.session["user_id"] = user.pk
            request.session["code"] = email.code
            request.session.set_expiry(0)

            return JsonResponse({"status": 200})

        return JsonResponse({"status": 403})


# Render PasswordReset View
class PasswordResetView(LogoutRequiredMixin, FormView):
    template_name = "account/password_reset.html"
    form_class = forms.PasswordResetForm
    success_url = reverse_lazy("account:password-reset")

    def form_valid(self, form):
        password_token = form.cleaned_data.get("password_token")

        # Build absolute url for password confirm page
        confirm_link = self.request.build_absolute_uri(
            reverse("account:password-reset-confirm") + f"?token={password_token.token}"
        )

        # Create new password_reset message
        email = CreateEmailMessage()
        email.password_reset_message(confirm_link)

        # Send email by async thread
        email_t = SendEmailThread(password_token.user, email.subject, email.message)
        email_t.start()

        messages.success(self.request, _("Reset password link sent to your email address."))
        return super().form_valid(form)


# PasswordResetConfirm View
class PasswordResetConfirmView(LogoutRequiredMixin, FormView):
    template_name = "account/password_reset_confirm.html"
    form_class = forms.PasswordResetConfirmForm
    success_url = reverse_lazy("account:password-reset-complete")

    def dispatch(self, request, *args, **kwargs):
        """ Check token validation before create form. Raise 404 error if token expired """
        token = request.GET.get("token")

        try:
            password_token = PasswordResetToken.objects.get(token=token)
            if password_token.expired_at < timezone.now():
                raise Http404("Page does not exists anymore")
        except PasswordResetToken.DoesNotExist:
            raise Http404("Page does not exists anymore")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ Change user password and delete token """

        password = form.cleaned_data.get("password")
        token = self.request.GET.get("token")

        try:
            password_token = PasswordResetToken.objects.get(token=token)
            user = password_token.user
            user.set_password(password)
            user.save()
        except (PasswordResetToken.DoesNotExist, User.DoesNotExist):
            raise Http404("Page does not exists anymore")

        # Delete password reset token
        password_token.delete()

        return super().form_valid(form)
