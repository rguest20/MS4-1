from django.urls import path

from . import views

app_name = 'ticketing'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('account/password', views.passwordupdate, name='password'),
    path('account/notification', views.notificationsettings, name='notification'),
    path('copyright/', views.copyright, name='copyright'),
    path('terms/', views.terms, name='terms'),
    path('report/', views.report, name='report'),
    path('support/', views.support, name='support'),
    path('support/ticket/{number}', views.supportticket, name='tickets'),
    path('contact/', views.contact, name='contact'),
    path('buy/', views.buy, name='buy')
]
