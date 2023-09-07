from django.views.generic import TemplateView


# Render MainView
class MainView(TemplateView):
    template_name = "main/index.html"
