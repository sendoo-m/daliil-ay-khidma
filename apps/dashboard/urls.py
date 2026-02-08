"""
Dashboard URLs
"""

from django.urls import path, include
from apps.dashboard.views import main as main_views
from apps.dashboard.views import business, product, deal, review

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', main_views.index, name='index'),
    path('', main_views.index, name='home'),  # Alias for compatibility
    
    # AJAX endpoints
    path('ajax/get-districts/', main_views.get_districts_by_governorate, name='ajax_get_districts'),
    
    # Business Management
    path('businesses/', business.business_list, name='business_list'),
    path('businesses/create/', business.business_create, name='business_create'),
    path('businesses/<slug:slug>/', business.business_detail, name='business_detail'),
    path('businesses/<slug:slug>/edit/', business.business_update, name='business_update'),
    path('businesses/<slug:slug>/delete/', business.business_delete, name='business_delete'),
    
    # Product Management
    path('products/', product.product_list, name='product_list'),
    path('products/create/', product.product_create, name='product_create'),
    path('products/<int:pk>/edit/', product.product_update, name='product_update'),
    path('products/<int:pk>/delete/', product.product_delete, name='product_delete'),
    
    # Deal Management
    path('deals/', deal.deal_list, name='deal_list'),
    path('deals/create/', deal.deal_create, name='deal_create'),
    path('deals/<int:pk>/edit/', deal.deal_update, name='deal_update'),
    path('deals/<int:pk>/delete/', deal.deal_delete, name='deal_delete'),
    
    # Review Management
    path('reviews/', review.review_list, name='review_list'),
    path('reviews/<int:pk>/reply/', review.review_reply, name='review_reply'),
    
    # Admin dashboard
    path('admin/', include('apps.dashboard.urls_admin')),
    
    # Owner dashboard
    path('owner/', include('apps.dashboard.urls_owner')),
]
