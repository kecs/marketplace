from datetime import timedelta, date, datetime
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db.models import Q
from django.template.defaultfilters import truncatewords


# Utils

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


class AuctionManager(models.Manager):
    def to_close(self):
        now = datetime.now()
        query = Q(Q(Q(duration=30) & Q(start_date__lt=now - timedelta(days=30))) |
                  Q(Q(duration=60) & Q(start_date__lt=now - timedelta(days=60))) |
                  Q(Q(duration=15) & Q(start_date__lt=now - timedelta(days=15))))
    
        super().get_queryset().filter(query)
        
    def open(self):
        return super().get_queryset().filter(is_open=True)

    def real_price(self, price_gte=None, price_lte=None):
        """
        Fiter auctionss, that are still open, according to duration and starting date,
        starting or current price is used, where possible.
        """
        query = Q(is_open=True)
        
        if price_gte:
            query &= Q(Q(Q(actual_price=0) & Q(starting_price__gte=price_gte)) |
                       Q(~Q(actual_price=0) & Q(actual_price__gte=price_gte)))
        if price_lte:
            query &= Q(Q(Q(actual_price=0) & Q(starting_price__lte=price_lte)) |
                       Q(~Q(actual_price=0) & Q(actual_price__lte=price_lte)))

        return super().get_queryset().filter(query)

    
def get_upload_to_path(instance, filename):
    path = f'{settings.UPLOADS_DIR}/auction_'
    path += f'{datetime.now().strftime("%Y_%m_%d")}_'
    path += f'{instance.title_slug}_'
    return path + filename

# Models

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
        reviews = self.reviewed_by_buyer.all()
        ratings_count = len(reviews)
        if ratings_count:
            return sum([r.stars for r in reviews]) / ratings_count
        else:
            return 0
    
    def __str__(self):
        return self.username
    

class Brand(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    
class Auction(models.Model):    
    title = models.CharField(max_length=255)
    description = models.TextField()
    product_condition = models.IntegerField(choices=CONDITION_CHOICES, default=1)
    brand = models.ForeignKey(Brand, models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, models.SET_NULL, null=True, blank=True)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=30)
    starting_price = models.PositiveIntegerField()
    actual_price = models.PositiveIntegerField(blank=True, null=True, default=0)
    start_date = models.DateField(auto_now_add=True)
    is_open = models.BooleanField(blank=True, default=True)
    img1 = models.ImageField(upload_to=get_upload_to_path)
    img2 = models.ImageField(upload_to=get_upload_to_path, blank=True, null=True)
    img3 = models.ImageField(upload_to=get_upload_to_path, blank=True, null=True)
    seller = models.ForeignKey(MarketplaceUser,
                               on_delete=models.CASCADE,
                               related_name='auctions',
                               blank=True, null=True)
    highest_bidder = models.ForeignKey(MarketplaceUser,
                                       related_name='highest_bids',
                                       on_delete=models.SET_NULL,
                                       blank=True, null=True)
    objects = AuctionManager()
    
    def get_upload_to_path(self, filename):
        path = f'{settings.UPLOADS_DIR}/auction_'
        path += f'{datetime.now().strftime("%Y_%m_%d")}_'
        path += f'{self.title_slug}_'
        return path + filename

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

    @property
    def real_price(self):
        if self.actual_price == 0:
            return self.starting_price
        else:
            return self.actual_price
        
    @property
    def open_until(self):
        return self.start_date + timedelta(days=self.duration)
    
    @property
    def short_description(self):
        if len(self.description) > 100:
            return truncatewords(self.description, 15) + ' ...'
        else:
            return self.description
    
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
        return self.watch_set.count()
    
    @property
    def likes(self):
        return self.like_set.count()

    def is_liked_by_user(self, user):
        return self.like_set.filter(marketplaceuser=user).count()
    
    def is_watched_by_user(self, user):
        return self.watch_set.filter(marketplaceuser=user).count()

    
class FKToUserAndAuction(models.Model):
    auction = models.ForeignKey(Auction, models.SET_NULL, blank=True, null=True)
    marketplaceuser = models.ForeignKey(MarketplaceUser,
                                        models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.marketplaceuser} : {self.auction}'

    
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
