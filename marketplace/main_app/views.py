# from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin

from .forms import AuctionForm
from .models import Auction, Like, Watch


class TOSView(TemplateView):
    template_name = "tos.html"


class LikeOrWatchView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Auction
    
    def post(self, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        
        if obj:
            self.to_create_model.objects.get_or_create(
                marketplaceuser=self.request.user,
                auction=obj)
            
            return JsonResponse({'msg': _('ok')})
        else:
            return JsonResponse({'msg': _('not found')}, status=404)

    
class WatchView(LikeOrWatchView):
    to_create_model = Watch
    

class LikeView(LikeOrWatchView):
    to_create_model = Like


class LandingView(LoginRequiredMixin, TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_items'] = Auction.objects.open()[:4]
        return context


class SellView(LoginRequiredMixin, CreateView):
    template_name = 'sell.html'
    form_class = AuctionForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.save()
        
        messages.success(self.request, _('Item successfully uploaded!'))

        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Auction
    template_name = 'detail.html'
