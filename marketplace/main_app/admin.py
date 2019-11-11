from django.contrib import admin

from .models import (MarketplaceUser, Brand, City, Auction, Like, Watch,
                     Review, TermsOfUse)


admin.site.register(MarketplaceUser)
admin.site.register(Brand)
admin.site.register(City)
admin.site.register(Auction)
admin.site.register(Like)
admin.site.register(Watch)
admin.site.register(Review)
admin.site.register(TermsOfUse)
