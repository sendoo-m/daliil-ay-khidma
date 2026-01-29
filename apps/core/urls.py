# apps/core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('test-icons/', views.test_icons, name='test_icons'),
    path('change-language/', views.change_language, name='change_language'),  # ← جديد
]
