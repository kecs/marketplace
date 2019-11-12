from django import template
from django.urls import reverse
from django.utils.translation import gettext as _


register = template.Library()


def is_done_by_user(verb, fn, auction, user):
    return {'num': getattr(auction, fn)(user),
            'verb': verb,
            'text': _(verb),
            'pk': auction.pk,
            'url': reverse(verb, kwargs={'pk': auction.pk})}


@register.inclusion_tag('detail_tag.html')
def is_liked_by_user(auction, user):
    return is_done_by_user('like', 'is_liked_by_user', auction, user)


@register.inclusion_tag('detail_tag.html')
def is_watched_by_user(auction, user):
    return is_done_by_user('watch', 'is_watched_by_user', auction, user)
