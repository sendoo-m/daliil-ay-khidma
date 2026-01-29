"""
Dashboard URLs
==============
روابط لوحات التحكم
"""

from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    # Owner Dashboard
    path('owner/', include('apps.dashboard.urls_owner')),
    
    # Admin Dashboard
    path('admin-panel/', include('apps.dashboard.urls_admin')),
]
