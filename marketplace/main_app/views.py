# from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import AuctionForm


class TOSView(TemplateView):
    template_name = "tos.html"


class LandingView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = 69
        return context


class SellView(CreateView):
    template_name = 'sell.html'
    form_class = AuctionForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.save()
        
        messages.success(self.request, _('Item successfully uploaded!'))

        return super().form_valid(form)
