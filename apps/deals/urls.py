"""
Deals URLs
==========
مسارات تطبيق العروض
"""

from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    # Public URLs
    path('', views.deal_list, name='deal_list'),
    path('detail/<slug:slug>/', views.deal_detail, name='deal_detail'),
    path('business/<slug:business_slug>/', views.deals_by_business, name='deals_by_business'),
    
    # User Actions
    path('claim/<slug:slug>/', views.claim_deal, name='claim_deal'),
    path('my/', views.my_deals, name='my_deals'),
    
    # Business Owner URLs
    path('manage/', views.business_deals, name='business_deals'),
    path('create/', views.deal_create, name='deal_create'),
    path('edit/<slug:slug>/', views.deal_edit, name='deal_edit'),
    path('delete/<slug:slug>/', views.deal_delete, name='deal_delete'),
    path('toggle/<slug:slug>/', views.deal_toggle_active, name='toggle_active'),
    path('claims/<slug:slug>/', views.deal_claims_list, name='deal_claims'),
]
