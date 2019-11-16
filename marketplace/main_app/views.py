# from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.shortcuts import render_to_response

from .forms import AuctionForm, SearchForm
from .models import Auction, Like, Watch


class BaseMixin(LoginRequiredMixin, SingleObjectMixin):
    pass


class TOSView(TemplateView):
    template_name = "tos.html"


class AuctionListView(LoginRequiredMixin, ListView):
    model = Auction
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'form': SearchForm(self.request.GET)})
        return ctx

    def updateQuery(self, name, q, _int=False):
        if _int:
            field = int(self.request.GET.get(name) or '0')
        else:
            field = self.request.GET.get(name).strip()
            
        if field:
            self.query.update({q: field})
    
    def get_queryset(self):
        self.query = {}

        # TODO: differentiate bw act pr and not having act pr, union 2 sep queries
        
        if self.actual_price:
            price_param = 'actual_price'
        else:
            price_param = 'starting_price'
            
        query_params = (('title', 'title__icontains', False),
                        ('price_from', price_param + '__gte', True),
                        ('price_to', price_param + '__lte', True),
                        ('brand', 'brand__name__icontains', False),
                        ('city', 'city__name__icontains', False), )
        
        for title, param, _int in query_params:
            self.updateQuery(title, param, _int)

        return Auction.objects.open().filter(**self.query).order_by('-start_date')
            
    
class LikeOrWatchView(BaseMixin, View):
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

    
class WatchView(BaseMixin, View):
    to_create_model = Watch
    

class LikeView(BaseMixin, View):
    to_create_model = Like


class BidView(BaseMixin, View):
    model = Auction
    template_name = 'detail.html'

    def respond(self, auction_id):
        return HttpResponseRedirect(reverse('product_detail', args=(auction_id, )))
    
    def post(self, *args, **kwargs):
        bid = int(self.request.POST.get('bid', '0'))
        self.object = self.get_object(self.get_queryset())
        
        # No bid
        if not bid:
            messages.error(self.request, _('Empty bid is not allowed!'), extra_tags='danger')
            return self.respond(self.object.id)        
        if self.object:
            # Auction found, invalid bid
            if bid <= self.object.actual_price:
                messages.error(self.request,
                               _('Your bid has to be higher than the current highest bid!'), extra_tags='danger')
                return self.respond(self.object.id)
            else:
                # Do not update closed auction!
                if not object.is_open:
                    messages.error(self.request, _('Auction is over!'), extra_tags='danger')
                    return self.respond(self.object.id)
                
                # Highest bidder
                self.object.highest_bidder = self.request.user
                self.object.actual_price = bid
                self.object.save()
            
                messages.success(self.request, _('You placed a bid!'))
                return self.respond(self.object.id)
            
        # Auction 404
        else:
            messages.error(self.request, _('Auction cannot be found!'),
                           extra_tags='danger')
            return HttpResponseRedirect(reverse('landing'))
    
    
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
