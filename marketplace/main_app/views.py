# from django.shortcuts import render
from django.views.generic import TemplateView


class TOSView(TemplateView):
    template_name = "tos.html"


class LandingView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = 69
        return context
