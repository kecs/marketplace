from django.contrib import admin

from .models import (MarketplaceUser, Brand, City, Auction, Like, Watch,
                     Review, TermsOfUse)


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'starting_price', 'actual_price', 'is_open')


admin.site.register(MarketplaceUser)
admin.site.register(Brand)
admin.site.register(City)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Like)
admin.site.register(Watch)
admin.site.register(Review)
admin.site.register(TermsOfUse)
