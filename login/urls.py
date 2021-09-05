from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from . import views
from django.urls import include, re_path

app_name = 'login'
urlpatterns = [
    path('', views.index, name='loginindex'),
    path('register/', views.register, name='register'),
    path('tinymce/', include('tinymce.urls')),
]
