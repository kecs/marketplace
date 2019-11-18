from __future__ import absolute_import, unicode_literals
from celery import task
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from .models import Auction


@task()
def close_auctions():
    # Auctions that should be closed, but are still open
    objects = Auction.objects.to_close().filter(is_open=True)
    objects.update(is_open=False)
    
    for auction in objects:
        send_mail(
            _('Congratulations! You have won an auction!'),
            _('You have won "fuckface"!'),
            # _(f'You have won "{auction.title}"!'),
            'marketplace@mihaly.gabor.com',
            [auction.highest_bidder.email],
            fail_silently=False,)
