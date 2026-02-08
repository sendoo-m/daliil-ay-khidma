"""
Dashboard URLs
"""

from django.urls import path, include
from apps.dashboard.views import main as main_views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', main_views.index, name='index'),
    
    # AJAX endpoints
    path('ajax/get-districts/', main_views.get_districts_by_governorate, name='ajax_get_districts'),
    
    # Admin dashboard
    path('admin/', include('apps.dashboard.urls_admin')),
    
    # Owner dashboard
    path('owner/', include('apps.dashboard.urls_owner')),
]
