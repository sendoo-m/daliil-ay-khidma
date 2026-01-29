"""
Dashboard URLs
=============
لوحة تحكم أصحاب المحلات
"""

from django.urls import path
from .views import (
    dashboard_home,
    # Business
    business_list, business_create, business_update, business_detail, business_delete,
    # Products
    product_list, product_create, product_update, product_delete,
    # Deals
    deal_list, deal_create, deal_update, deal_delete,
    # Reviews
    review_list, review_reply,
    # Stats
    dashboard_stats,
)

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', dashboard_home, name='home'),
    path('stats/', dashboard_stats, name='stats'),
    
    # Business Management
    path('businesses/', business_list, name='business_list'),
    path('businesses/create/', business_create, name='business_create'),
    path('businesses/<slug:slug>/', business_detail, name='business_detail'),
    path('businesses/<slug:slug>/update/', business_update, name='business_update'),
    path('businesses/<slug:slug>/delete/', business_delete, name='business_delete'),
    
    # Product Management
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/<slug:slug>/update/', product_update, name='product_update'),
    path('products/<slug:slug>/delete/', product_delete, name='product_delete'),
    
    # Deal Management
    path('deals/', deal_list, name='deal_list'),
    path('deals/create/', deal_create, name='deal_create'),
    path('deals/<slug:slug>/update/', deal_update, name='deal_update'),
    path('deals/<slug:slug>/delete/', deal_delete, name='deal_delete'),
    
    # Review Management
    path('reviews/', review_list, name='review_list'),
    path('reviews/<int:pk>/reply/', review_reply, name='review_reply'),
]
