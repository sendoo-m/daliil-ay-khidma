"""
Owner Dashboard URLs
====================
روابط لوحة التحكم - أصحاب المحلات
"""

from django.urls import path
from apps.dashboard.views import owner

app_name = 'owner'

urlpatterns = [
    # Dashboard Home
    path('', owner.owner_dashboard, name='dashboard'),
    
    # Business Management
    path('businesses/', owner.business_list, name='business_list'),
    path('businesses/create/', owner.business_create, name='business_create'),
    path('businesses/<slug:slug>/edit/', owner.business_edit, name='business_edit'),
    path('businesses/<slug:slug>/delete/', owner.business_delete, name='business_delete'),
    
    # Product Management
    path('products/', owner.product_list, name='product_list'),
    path('products/create/', owner.product_create, name='product_create'),
    path('products/<slug:slug>/edit/', owner.product_edit, name='product_edit'),
    path('products/<slug:slug>/delete/', owner.product_delete, name='product_delete'),
    
    # Deal Management
    path('deals/', owner.deal_list, name='deal_list'),
    path('deals/create/', owner.deal_create, name='deal_create'),
    path('deals/<slug:slug>/edit/', owner.deal_edit, name='deal_edit'),
    path('deals/<slug:slug>/delete/', owner.deal_delete, name='deal_delete'),
    
    # Reviews Management
    path('reviews/', owner.review_list, name='review_list'),
    path('reviews/<int:pk>/respond/', owner.review_respond, name='review_respond'),
]
