"""
Admin Dashboard URLs
====================
URLs for admin dashboard - full control panel
"""

from django.urls import path
from .views import admin_views

app_name = 'admin_dashboard'

urlpatterns = [
    # Admin Dashboard Home
    path('', admin_views.admin_dashboard_home, name='home'),
    
    # Statistics & Analytics
    path('analytics/', admin_views.admin_analytics, name='analytics'),
    path('reports/', admin_views.admin_reports, name='reports'),
    
    # Users Management
    path('users/', admin_views.admin_users_list, name='users_list'),
    path('users/<int:user_id>/', admin_views.admin_user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/', admin_views.admin_user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', admin_views.admin_user_delete, name='user_delete'),
    path('users/<int:user_id>/toggle-status/', admin_views.admin_user_toggle_status, name='user_toggle_status'),
    
    # Businesses Management
    path('businesses/', admin_views.admin_businesses_list, name='businesses_list'),
    path('businesses/<int:business_id>/', admin_views.admin_business_detail, name='business_detail'),
    path('businesses/<int:business_id>/verify/', admin_views.admin_business_verify, name='business_verify'),
    path('businesses/<int:business_id>/feature/', admin_views.admin_business_feature, name='business_feature'),
    path('businesses/<int:business_id>/toggle-status/', admin_views.admin_business_toggle_status, name='business_toggle_status'),
    path('businesses/<int:business_id>/delete/', admin_views.admin_business_delete, name='business_delete'),
    
    # Products Management
    path('products/', admin_views.admin_products_list, name='products_list'),
    path('products/<int:product_id>/', admin_views.admin_product_detail, name='product_detail'),
    path('products/<int:product_id>/toggle-status/', admin_views.admin_product_toggle_status, name='product_toggle_status'),
    path('products/<int:product_id>/feature/', admin_views.admin_product_feature, name='product_feature'),
    path('products/<int:product_id>/delete/', admin_views.admin_product_delete, name='product_delete'),
    
    # Deals Management
    path('deals/', admin_views.admin_deals_list, name='deals_list'),
    path('deals/<int:deal_id>/', admin_views.admin_deal_detail, name='deal_detail'),
    path('deals/<int:deal_id>/approve/', admin_views.admin_deal_approve, name='deal_approve'),
    path('deals/<int:deal_id>/feature/', admin_views.admin_deal_feature, name='deal_feature'),
    path('deals/<int:deal_id>/delete/', admin_views.admin_deal_delete, name='deal_delete'),
    
    # Reviews Management
    path('reviews/', admin_views.admin_reviews_list, name='reviews_list'),
    path('reviews/<int:review_id>/approve/', admin_views.admin_review_approve, name='review_approve'),
    path('reviews/<int:review_id>/reject/', admin_views.admin_review_reject, name='review_reject'),
    path('reviews/<int:review_id>/delete/', admin_views.admin_review_delete, name='review_delete'),
    
    # Categories Management
    path('categories/', admin_views.admin_categories_list, name='categories_list'),
    path('categories/create/', admin_views.admin_category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', admin_views.admin_category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', admin_views.admin_category_delete, name='category_delete'),
    
    # System Settings
    path('settings/', admin_views.admin_settings, name='settings'),
    path('settings/cache/clear/', admin_views.admin_clear_cache, name='clear_cache'),
]
