from django.utils.translation import gettext as _
from django import forms

from .models import Password, Card


# AddPassword form
class AddPasswordForm(forms.ModelForm):
    class Meta:
        model = Password
        exclude = ["user", "difficulty", "type", "is_archived"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5",
                "placeholder": _("Capsule digital market"),
                "id": "title",
                "name": "title",
            }),
            "address": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5",
                "placeholder": "something.com",
                "id": "address",
                "name": "address",
            }),
            "username": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5 ss01",
                "placeholder": "example@email.com",
                "id": "username",
                "name": "username",
            }),
            "password": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 w-full border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5 ss01",
                "placeholder": "123456",
                "id": "password",
                "name": "password",
            }),
            "name": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5",
                "id": "name",
                "name": "name"
            }),
            "melli": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 w-full border-2 focus:outline-none focus:ring-0 rounded-lg px-2 py-1.5 ss01",
                "id": "melli-code",
                "name": "melli"
            })
        }


# AddCard form
class AddCardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ["user", "is_archived"]

        widgets = {
            "bank": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5",
                "id": "bank",
                "name": "bank",
            }),
            "c_number": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 text-center ltr border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5 ss01",
                "placeholder": "0000 0000 0000 0000",
                "id": "card-number",
                "name": "c_number",
            }),
            "cvv2": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 grow text-center ltr border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5 ss01",
                "placeholder": "0000",
                "id": "cvv2",
                "name": "cvv2",
            }),
            "exp_month": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 text-center ltr border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5 ss01",
                "placeholder": "01",
                "id": "month-exp",
                "name": "exp_month",
            }),
            "exp_year": forms.TextInput(attrs={
                "class": "text-slate-800 focus:border-gray-400 text-center ltr border-2 focus:outline-none focus:ring-0 placeholder:opacity-80 rounded-lg px-2 py-1.5 ss01",
                "placeholder": "01",
                "id": "year-exp",
                "name": "exp_year",
            }),
        }

    def clean_c_number(self):
        c_number = self.cleaned_data.get("c_number")
        c_number = c_number.replace(" ", "")

        return c_number
