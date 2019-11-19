from django.conf.urls.static import static
from django.conf import settings

"""marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main_app.views import (LandingView, TOSView, SellView, AuctionListView,
                            ProductDetailView, WatchView, LikeView, BidView,
                            ProfileView)


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tos', TOSView.as_view(), name="tos"),
    path('sell', SellView.as_view(), name="sell"),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
    path('watch/<int:pk>/', WatchView.as_view(), name="watch"),
    path('like/<int:pk>/', LikeView.as_view(), name="like"),
    path('bid/<int:pk>/', BidView.as_view(), name="bid"),
    path('search/', AuctionListView.as_view(), name="search"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('', LandingView.as_view(), name='landing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.UPLOADS_DIR, document_root=settings.UPLOADS_DIR)
