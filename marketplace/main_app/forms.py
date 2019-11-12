from datetime import date

from django.forms import ModelForm, CharField

from .models import MarketplaceUser, Auction, City, Brand


class AuctionForm(ModelForm):
    brand = CharField()
    city = CharField()

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['brand'] = cleaned_data['brand'].strip().lower()
        cleaned_data['city'] = cleaned_data['city'].strip().lower()

        return cleaned_data

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.brand = Brand.objects.get_or_create(name=self.cleaned_data['brand'])[0]
        instance.city = City.objects.get_or_create(name=self.cleaned_data['city'])[0]
        instance.save()
        
        return instance

    class Meta:
        model = Auction
        exclude = ['actual_price', 'highest_bidder', 'seller',
                   'brand', 'city',
                   'start_date',]


