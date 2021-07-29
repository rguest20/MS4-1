from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from . import views
from django.urls import include, re_path

app_name = 'purchasing'
urlpatterns = [
    path('buy/', views.buy, name='buy'),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path("webhook/", views.stripe_webhook, name="webhook"),
    path('success/', views.success, name='success'),
    path('deleted/', views.deleted, name='deleted'),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
