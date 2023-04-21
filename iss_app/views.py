from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "iss_app/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
