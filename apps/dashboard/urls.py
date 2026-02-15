"""Add missing deal URL patterns to fix NoReverseMatch
Dashboard URLs
"""
from django.urls import path, include
from apps.dashboard.views import main as main_views
from aFixed NoReverseMatch error in dashboard templates by adding 'deal_list' and other missing deal URL patterns.pps.dashboard.views import business, product, deal, review

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', main_views.index, name='index'),
    path('', main_views.index, name='home'),  # Alias for compatibility

    # AJAX endpoints
    path('ajax/get-cities/', main_views.get_cities_by_governorate, name='get_cities_by_governorate'),
    path('ajax/get-districts/', main_views.get_districts_by_city, name='get_districts_by_city'),
    path('ajax/get-districts-legacy/', main_views.get_districts_by_governorate, name='get_districts_by_governorate'),

    # Stats & Profile
    path('stats/', main_views.index, name='stats'),  # Placeholder - redirect to index
    path('profile/', main_views.profile, name='profile'),
    path('settings/', main_views.settings, name='settings'),
    path('notifications/', main_views.notifications, name='notifications'),
    path('help/', main_views.help_center, name='help'),

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
]
