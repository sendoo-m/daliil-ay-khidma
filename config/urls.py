"""
Main URL Configuration
======================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Dashboard URLs
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    
    # API URLs
    path('api/v1/', include('apps.api.urls', namespace='api')),
    
    # Account URLs (Login, Register, etc.)
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    
    # Directory URLs (Homepage, Businesses, etc.)
    # path('', include('apps.directory.urls', namespace='directory')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
