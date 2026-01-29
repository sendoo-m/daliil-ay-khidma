"""
URL configuration for daliil-ay-khidma project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # REST API
    path('api/v1/', include('apps.api.urls')),
    
    # Core apps
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('services/', include('apps.services.urls')),
    path('categories/', include('apps.categories.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('search/', include('apps.search.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    
    # Feature apps
    path('products/', include('apps.products.urls')),
    path('deals/', include('apps.deals.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Admin site customization
admin.site.site_header = 'دليل أي خدمة - لوحة التحكم'
admin.site.site_title = 'دليل أي خدمة'
admin.site.index_title = 'إدارة النظام'
