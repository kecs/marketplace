from datetime import timedelta, datetime
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


CONDITION_CHOICES = (
    (1, _("New")),
    (2, _("Excellent")),
    (3, _("Used")),
    (4, _("As pictured")),
)


DURATION_CHOICES = (
    (30, _("One month")),
    (60, _("Two month")),
    (15, _("One week")),
)

def get_upload_to_path(instance, filename):
    path = f'{settings.UPLOADS_DIR}/auction_'
    path += f'{datetime.now().strftime("%Y_%m_%d")}_'
    return path + f'{instance.title_slug}'


class City(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    
class MarketplaceUser(AbstractUser):
    address = models.CharField(max_length=512)
    did_accept_tos = models.BooleanField(default=False, blank=True)
    member_since = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=1024)
    city = models.ForeignKey(City, models.SET_NULL, null=True)

    @property
    def rating(self):
        reviews = self.review__set.objects.all()
        ratings_count = len(reviews)
        if ratings_count:
            return sum([r.value for r in reviews]) / ratings_count
    
    def __str__(self):
        return self.username
    

class Brand(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    
class Auction(models.Model):
    title = models.CharField(max_length=255)
    product_condition = models.IntegerField(choices=CONDITION_CHOICES, default=1)
    brand = models.ForeignKey(Brand, models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, models.SET_NULL, null=True)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=30)
    starting_price = models.IntegerField()
    actual_price = models.IntegerField()
    start_date = models.DateField()
    img1 = models.ImageField(upload_to=get_upload_to_path)
    img2 = models.ImageField(upload_to=get_upload_to_path)
    img3 = models.ImageField(upload_to=get_upload_to_path)

    seller = models.ForeignKey(MarketplaceUser,
                               on_delete=models.CASCADE,
                               related_name='auctions')
    highest_bidder = models.ForeignKey(MarketplaceUser,
                                       related_name='highest_bids',
                                       on_delete=models.SET_NULL,
                                       blank=True, null=True)

    @property
    def title_slug(self):
        return slugify(self.title)
    
    def __str__(self):
        return f"{self.title} [{self.duration} {_('days')}]"
    
    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.duration)

    @property
    def watchers(self):
        return self.watch__set.count()
    
    @property
    def likes(self):
        return self.like__set.count()
    
    
class FKToUserAndAuction(models.Model):
    auction = models.ForeignKey(Auction, models.SET_NULL, blank=True, null=True)
    marketplaceuser = models.ForeignKey(MarketplaceUser,
                                        models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True

    
class Like(FKToUserAndAuction): pass


class Watch(FKToUserAndAuction): pass


class Review(models.Model):
    auction = models.ForeignKey(Auction, models.SET_NULL, blank=True, null=True)
    stars = models.IntegerField(choices=((i, i) for i in range(6)))
    review = models.TextField(blank=True, default='')
    seller = models.ForeignKey(MarketplaceUser,
                               related_name='reviewed_by_buyer',
                               on_delete=models.CASCADE)
    buyer = models.ForeignKey(MarketplaceUser,
                              related_name='reviewed_by_seller',
                              on_delete=models.SET_NULL, null=True)

    
class TermsOfUse(models.Model):
    text = models.TextField()
