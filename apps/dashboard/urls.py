"""
Dashboard URLs
=============
URL patterns for Owner and Admin dashboards
"""

from django.urls import path
from apps.dashboard.views import owner, admin

app_name = 'dashboard'

urlpatterns = [
    # ========================================
    # Owner Dashboard
    # ========================================
    path('', owner.owner_dashboard, name='owner_dashboard'),
    
    # Business Management
    path('businesses/', owner.business_list, name='business_list'),
    path('businesses/create/', owner.business_create, name='business_create'),
    path('businesses/<slug:slug>/', owner.business_detail, name='business_detail'),
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
    
    # Review Management
    path('reviews/', owner.review_list, name='review_list'),
    path('reviews/<int:pk>/reply/', owner.review_reply, name='review_reply'),
    
    # ========================================
    # Admin Dashboard
    # ========================================
    path('admin/', admin.admin_dashboard, name='admin_dashboard'),
    
    # User Management
    path('admin/users/', admin.admin_user_list, name='admin_user_list'),
    path('admin/users/<int:pk>/', admin.admin_user_detail, name='admin_user_detail'),
    path('admin/users/<int:pk>/toggle-active/', admin.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('admin/users/<int:pk>/delete/', admin.admin_user_delete, name='admin_user_delete'),
    
    # Business Management
    path('admin/businesses/', admin.admin_business_list, name='admin_business_list'),
    path('admin/businesses/<slug:slug>/verify/', admin.admin_business_verify, name='admin_business_verify'),
    path('admin/businesses/<slug:slug>/toggle-active/', admin.admin_business_toggle_active, name='admin_business_toggle_active'),
    path('admin/businesses/<slug:slug>/delete/', admin.admin_business_delete, name='admin_business_delete'),
    
    # Category Management
    path('admin/categories/', admin.admin_category_list, name='admin_category_list'),
    
    # Location Management
    path('admin/locations/', admin.admin_location_list, name='admin_location_list'),
    
    # Review Management
    path('admin/reviews/', admin.admin_review_list, name='admin_review_list'),
    path('admin/reviews/<int:pk>/approve/', admin.admin_review_approve, name='admin_review_approve'),
    path('admin/reviews/<int:pk>/delete/', admin.admin_review_delete, name='admin_review_delete'),
    
    # Product Management
    path('admin/products/', admin.admin_product_list, name='admin_product_list'),
    path('admin/products/<slug:slug>/delete/', admin.admin_product_delete, name='admin_product_delete'),
    
    # Deal Management
    path('admin/deals/', admin.admin_deal_list, name='admin_deal_list'),
    path('admin/deals/<slug:slug>/toggle-featured/', admin.admin_deal_toggle_featured, name='admin_deal_toggle_featured'),
    path('admin/deals/<slug:slug>/delete/', admin.admin_deal_delete, name='admin_deal_delete'),
]
