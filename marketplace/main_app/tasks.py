from __future__ import absolute_import, unicode_literals
from celery import task
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from .models import Auction


@task()
def close_auctions():
    # Auctions that should be closed, but are still open
    objects = Auction.objects.to_close().filter(is_open=True)

    if not len(objects):
        return
    
    objects.update(is_open=False)
    
    for auction in objects:
        send_mail(
            _('Congratulations! You have won an auction!'),
            _(f'You have won "{auction.title}"! Get in touch with the seller: {auction.seller.email}.'),
            'marketplace@google.cloud.com',
            [auction.highest_bidder.email],
            fail_silently=False,)

        if auction.highest_bidder:
            send_mail(
                _('Your auction is over.'),
                _(f'Your item "{auction.title}"\'s highest bid came from {auction.highest_bidder.email} (auction.real_price).'),
                'marketplace@google.cloud.com',
                [auction.highest_bidder.email],
                fail_silently=False,)
        else:
            send_mail(
                _('Your auction is over.'),
                _(f'Your item "{auction.title}" did not receive any bids.'),
                'marketplace@google.cloud.com',
                [auction.highest_bidder.email],
                fail_silently=False,)
