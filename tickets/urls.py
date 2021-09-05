from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from . import views
from django.urls import include, re_path

app_name = 'ticketing'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('copyright/', views.copyright, name='copyright'),
    path('terms/', views.terms, name='terms'),
    path('report/', views.report, name='report'),
    path('support/', views.support, name='support'),
    path('support/<int:number>/', views.supportticket, name='ticket'),
    path('support/edit/<int:number>/', views.editticket, name='editticket'),
    path('support/<int:number>/mark', views.markticket, name='markticket'),
    path('comment/<int:number>/', views.comment, name='comment'),
    path('comment/<int:number>/post/', views.comment_post, name='comment-post'),
    path('contact/', views.contact, name='contact'),
    path('account/password', auth_views.PasswordChangeView.as_view(template_name='tickets/account/passwordupdate.html', success_url='/dashboard/')),
    path('account/password/done', auth_views.PasswordChangeDoneView.as_view()),
    path('tinymce/', include('tinymce.urls')),
    path('dashboard/admin/tickets/', views.admin_tickets, name='admin-tickets'),
    path('dashboard/admin/tickets/<int:number>', views.admin_tickets_single, name='admin-tickets-single'),
    path('dashboard/admin', views.dashboard_admin, name='dashboard-admin'),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
