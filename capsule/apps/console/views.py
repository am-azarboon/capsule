from django.views.generic import TemplateView, FormView, UpdateView, DeleteView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import AddPasswordForm, AddCardForm
from .validators import pass_difficulty_ave
from .models import Password, Card
from itertools import chain


# Render DashboardView
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "console/dashboard.html"

    def get_context_data(self, **kwargs):
        """ Return 3 latest added passwords and cards. Return passwords average quality. """

        contexts = super().get_context_data(**kwargs)

        passwords = Password.objects.filter(user=self.request.user).order_by("-created_at")
        cards = Card.objects.filter(user=self.request.user).order_by("-created_at")
        objects = list(chain(passwords, cards))

        contexts["object_list"] = sorted(objects, key=lambda x: x.created_at, reverse=True)[:3]
        contexts["quality"] = pass_difficulty_ave(passwords)

        return contexts


# Render PasswordsView
class PasswordsView(LoginRequiredMixin, ListView):
    template_name = "console/passwords.html"

    def post(self, request):
        q = request.POST.get("q")
        passwords = Password.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(username__contains=q)) if q else None
        if not passwords:
            request.session["q"] = q
            return redirect("console:cards")

        return render(self.request, "console/passwords.html", {"object_list": passwords})

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user, is_archived=False)


# Render AddPasswordView
class AddPasswordView(LoginRequiredMixin, FormView):
    template_name = "console/pass_form.html"
    form_class = AddPasswordForm
    success_url = reverse_lazy("console:passwords")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        
        return super().form_valid(form)


# Render EditPasswordView
class EditPasswordView(LoginRequiredMixin, UpdateView):
    template_name = "console/pass_form.html"
    form_class = AddPasswordForm
    model = Password
    success_url = reverse_lazy("console:passwords")


# Render DeletePasswordView
class DeletePasswordView(LoginRequiredMixin, DeleteView):
    template_name = "console/object_confirm_delete.html"
    model = Password
    success_url = reverse_lazy("console:passwords")


# Render CardsView
class CardsView(LoginRequiredMixin, ListView):
    template_name = "console/cards.html"

    def get_queryset(self):
        q = self.request.session.get("q")
        if q:
            del self.request.session["q"]
            return Card.objects.filter(Q(bank__icontains=q) | Q(c_number__contains=q))

        return Card.objects.filter(user=self.request.user, is_archived=False)


# Render AddCardView
class AddCardView(LoginRequiredMixin, FormView):
    template_name = "console/card_form.html"
    form_class = AddCardForm
    success_url = reverse_lazy("console:cards")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        return super().form_valid(form)


# Render EditCardView
class EditCardView(LoginRequiredMixin, UpdateView):
    template_name = "console/card_form.html"
    form_class = AddCardForm
    model = Card
    success_url = reverse_lazy("console:cards")


# Render DeleteCardView
class DeleteCardView(LoginRequiredMixin, DeleteView):
    template_name = "console/object_confirm_delete.html"
    model = Card
    success_url = reverse_lazy("console:cards")


# Render ArchivesView
class ArchivesView(LoginRequiredMixin, ListView):
    template_name = "console/archives.html"

    def get_queryset(self):
        passwords = Password.objects.filter(user=self.request.user, is_archived=True)
        cards = Card.objects.filter(user=self.request.user, is_archived=True)

        return chain(passwords, cards)


# Render AddToArchiveView
class AddToArchiveView(LoginRequiredMixin, View):
    def get(self, request, pk):
        """ Get password or card with given pk and add to/remove it from archive list """

        try:
            password = Password.objects.get(pk=pk)
            if password.is_archived:
                password.is_archived = False
                password.save()
                return JsonResponse({"response": "unarchived"})

            password.is_archived = True
            password.save()

            return JsonResponse({"response": "archived"})
        except Password.DoesNotExist:
            card = Card.objects.get(pk=pk)

            if card.is_archived:
                card.is_archived = False
                card.save()
                return JsonResponse({"response": "unarchived"})

            card.is_archived = True
            card.save()

            return JsonResponse({"response": "archived"})
