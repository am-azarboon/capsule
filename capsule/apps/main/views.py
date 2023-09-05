from django.views.generic import TemplateView
from django.shortcuts import reverse


# Render MainView
class MainView(TemplateView):
    template_name = "main/index.html"
