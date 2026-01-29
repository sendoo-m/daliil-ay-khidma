"""
Admin Dashboard URLs
====================
روابط لوحة الإدارة
"""

from django.urls import path
from apps.dashboard.views import admin_panel

app_name = 'admin'

urlpatterns = [
    # Dashboard Home
    path('', admin_panel.admin_dashboard, name='dashboard'),
    
    # User Management
    path('users/', admin_panel.user_list, name='user_list'),
    path('users/create/', admin_panel.user_create, name='user_create'),
    path('users/<int:pk>/edit/', admin_panel.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', admin_panel.user_delete, name='user_delete'),
    
    # Business Management
    path('businesses/', admin_panel.admin_business_list, name='business_list'),
    path('businesses/<slug:slug>/edit/', admin_panel.admin_business_edit, name='business_edit'),
    path('businesses/<slug:slug>/verify/', admin_panel.admin_business_verify, name='business_verify'),
    
    # Product Management
    path('products/', admin_panel.admin_product_list, name='product_list'),
    
    # Location Management
    path('governorates/', admin_panel.governorate_list, name='governorate_list'),
    path('cities/', admin_panel.city_list, name='city_list'),
    path('districts/', admin_panel.district_list, name='district_list'),
    
    # Category Management
    path('categories/', admin_panel.category_list, name='category_list'),
    
    # Deal Management
    path('deals/', admin_panel.admin_deal_list, name='deal_list'),
]
