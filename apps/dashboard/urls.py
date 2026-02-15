"""
Dashboard URLs
"""
from django.urls import path, include
from apps.dashboard.views import main as main_views
from apps.dashboard.views import business
from apps.dashboard.views import product
from apps.dashboard.views import deal
from apps.dashboard.views import review

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', main_views.index, name='index'),
    path('home/', main_views.index, name='home'), # Alias for compatibility

    # Admin & Owner dashboards
    path('admin/', include('apps.dashboard.urls_admin', namespace='admin_dashboard')),
    path('owner/', include('apps.dashboard.urls_owner', namespace='owner')),

    # AJAX endpoints
    path('ajax/get-cities/', main_views.get_cities_by_governorate, name='get_cities_by_governorate'),
    path('ajax/get-districts/', main_views.get_districts_by_city, name='get_districts_by_city'),
    path('ajax/get-districts-legacy/', main_views.get_districts_by_governorate, name='get_districts_by_governorate_legacy'),

    # Stats & Profile
    path('stats/', main_views.index, name='stats'), # Placeholder - redirect to index
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
    path('products/<slug:slug>/edit/', product.product_update, name='product_update'),
    path('products/<slug:slug>/delete/', product.product_delete, name='product_delete'),

    # Deal Management
    path('deals/', deal.deal_list, name='deal_list'),
    path('deals/create/', deal.deal_create, name='deal_create'),
    path('deals/<slug:slug>/edit/', deal.deal_update, name='deal_update'),
    path('deals/<slug:slug>/delete/', deal.deal_delete, name='deal_delete'),

    # Reviews
    path('reviews/', review.review_list, name='review_list'),
    path('reviews/<int:pk>/reply/', review.review_reply, name='review_reply'),
    path('reviews/<int:pk>/approve/', review.review_approve, name='review_approve'),
    path('reviews/<int:pk>/reject/', review.review_reject, name='review_reject'),
]
