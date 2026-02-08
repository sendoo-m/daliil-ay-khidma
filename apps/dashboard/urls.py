"""
Dashboard URLs
"""

from django.urls import path, include
from apps.dashboard.views import main as main_views
from apps.dashboard.views import business

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', main_views.index, name='index'),
    path('', main_views.index, name='home'),  # Alias for compatibility
    
    # AJAX endpoints
    path('ajax/get-districts/', main_views.get_districts_by_governorate, name='ajax_get_districts'),
    
    # Business Management (direct access for owners)
    path('businesses/', business.business_list, name='business_list'),
    path('businesses/create/', business.business_create, name='business_create'),
    path('businesses/<slug:slug>/', business.business_detail, name='business_detail'),
    path('businesses/<slug:slug>/edit/', business.business_update, name='business_update'),
    path('businesses/<slug:slug>/delete/', business.business_delete, name='business_delete'),
    
    # Admin dashboard
    path('admin/', include('apps.dashboard.urls_admin')),
    
    # Owner dashboard
    path('owner/', include('apps.dashboard.urls_owner')),
]
