from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.utils import timezone
from django import forms

from .models import User, PasswordResetToken


# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={
        "class": "rounded-md text-start placeholder:text-right border-2 focus:border-gray-400 focus:outline-none focus:ring-0 py-2 px-3",
        "placeholder": _("Mobile number or email address"),
    }))
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput(attrs={
        "class": "w-full py-2 px-3 rounded-md text-right placeholder:text-right border-2 focus:border-gray-400 focus:outline-none",
        "placeholder": _("Password"),
        "id": "password",
    }))

    def clean(self):
        """ Authenticate and return user """

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if not user or User.objects.filter(username=username, verify=False).exists():
            raise ValidationError(_("Entered data is not correct!"), code="USER-NOT-EXISTS")

        return {"user": user}


# Register form
class RegisterForm(forms.Form):
    name = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={
        "class": "rounded-md text-right placeholder:text-right border-2 focus:border-gray-400 focus:outline-none focus:ring-0 py-2 px-3",
        "placeholder": _("FullName*"),
    }))
    email = forms.EmailField(max_length=64, required=True, widget=forms.EmailInput(attrs={
        "class": "rounded-md placeholder:text-right border-2 focus:border-gray-400 focus:outline-none focus:ring-0 py-2 px-3",
        "placeholder": _("Email Address*"),
    }))
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput(attrs={
        "class": "w-full py-2 px-3 text-right rounded-md placeholder:text-right border-2 focus:border-gray-400 focus:outline-none",
        "placeholder": _("Password*"),
        "id": "password",
    }))
    password2 = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput(attrs={
        "class": "w-full py-2 px-3 text-right rounded-md placeholder:text-right border-2 focus:border-gray-400 focus:outline-none",
        "placeholder": _("Repeat Password*"),
        "id": "password2",
    }))

    def clean_password2(self):
        """ Check passwords are the same. Raise Validation error if not. """

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password2 != password:
            raise ValidationError(_("Passwords are not match!"), code="PASSWORDS-NOT-MATCH")

        return self.cleaned_data

    def clean(self):
        """ Create and return new user """

        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if User.objects.filter(username=email, verify=True).exists():
            raise ValidationError(_("User is already exists!"))

        user = User.objects.get_or_create(username=email, verify=False)[0]
        user.full_name = name
        user.set_password(password)
        user.save()

        return {"user": user}


# EmailVerify form
class EmailVerifyForm(forms.Form):
    code = forms.CharField(max_length=5, required=True, widget=forms.TextInput(attrs={
        "class": "py-2 px-3 rounded-md text-center placeholder:text-right border-2 focus:border-slate-400 focus:outline-none ss01",
        "placeholder": _("Sent code"),
    }))


# PasswordReset form
class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=64, required=True, widget=forms.EmailInput(attrs={
        "class": "rounded-md placeholder:text-right border-2 focus:border-gray-400 focus:outline-none focus:ring-0 py-2 px-3",
        "placeholder": _("Email address"),
    }))

    def clean(self):
        """ Create and return password reset token """

        try:
            email = self.cleaned_data.get("email")
            user = User.objects.get(username=email, verify=True)

            # Return password reset token if already exists and not expired
            password_token = PasswordResetToken.objects.filter(user=user).first()
            if password_token and password_token.expired_at > timezone.now():
                return {"password_token": password_token}

            # Create new password reset token
            password_token = PasswordResetToken.objects.create(user=user)
            password_token.save()

            return {"password_token": password_token}

        except User.DoesNotExist:
            raise ValidationError(_("User with this email does not exists!"), code="USER-NOT-EXISTS")


# PasswordResetConfirm form
class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput(attrs={
        "class": "w-full py-2 px-3 text-right rounded-md placeholder:text-right border-2 focus:border-gray-400 focus:outline-none",
        "placeholder": _("Password*"),
        "id": "password",
    }))
    password2 = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput(attrs={
        "class": "w-full py-2 px-3 text-right rounded-md placeholder:text-right border-2 focus:border-gray-400 focus:outline-none",
        "placeholder": _("Repeat Password*"),
        "id": "password2",
    }))

    def clean_password2(self):
        """ Check passwords are the same. Raise Validation error if not. """

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password2 != password:
            raise ValidationError(_("Passwords are not match!"), code="PASSWORDS-NOT-MATCH")

        return self.cleaned_data["password"]


# UserProfile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image", "username", "full_name", "mobile", "melli"]

        widgets = {
            "image": forms.FileInput(attrs={
                "class": "hidden",
                "id": "image",
            }),
            "username": forms.EmailInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 rounded-lg px-2 py-1.5 ss01",
                "id": "username",
            }),
            "full_name": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none text-right focus:ring-0 rounded-lg px-2 py-1.5 ss01",
                "id": "name",
            }),
            "mobile": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5 ss01",
                "placeholder": _("Mobile number"),
                "id": "mobile",
            }),
            "melli": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 rounded-lg px-2 py-1.5 ss01",
                "id": "melli",
            }),
        }


# PasswordChange form
class PasswordChangeForm(forms.Form):
    user_password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "text-slate-800 w-full focus:border-gray-400 border-2 focus:outline-none text-right focus:ring-0 rounded-lg px-2 py-1.5 ss01",
        "id": "user_password",
    }))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "text-slate-800 w-full focus:border-gray-400 border-2 focus:outline-none text-right focus:ring-0 rounded-lg px-2 py-1.5 ss01",
        "id": "password",
    }))
    password2 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "text-slate-800 w-full focus:border-gray-400 border-2 focus:outline-none text-right focus:ring-0 rounded-lg px-2 py-1.5 ss01",
        "id": "password2",
    }))

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters."), code="PASSWORD-SHORT")

        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password2 != password:
            raise ValidationError(_("Passwords are not match!"), code="PASSWORDS-NOT-MATCH")

        return password
