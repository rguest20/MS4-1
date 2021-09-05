from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from . import views
from django.urls import include, re_path

app_name = 'clients'
urlpatterns = [
    path('account/', views.account, name='account'),
    path('account/edit', views.account_edit, name='account'),
    path('account/delete', views.delete, name='delete'),
    path('dashboard/admin/log/', views.admin_log, name='admin-log'),
    path('dashboard/admin/companies/', views.admin_companies, name='admin-companies'),
    path('dashboard/admin/companies/create_user/', views.admin_create_user, name='admin-create-user'),
    path('dashboard/admin/companies/create_company/', views.admin_create_company, name='admin-create-company'),
    path('deleted/', views.deleted, name='deleted'),
]
