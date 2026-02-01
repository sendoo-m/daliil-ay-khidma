# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('categories/', include('apps.categories.urls', namespace='categories')),
    path('directory/', include('apps.directory.urls', namespace='directory')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('deals/', include('apps.deals.urls', namespace='deals')),
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),
    path('api/v1/', include('apps.api.urls', namespace='api')),
]

# Static & Media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug Toolbar (Development only)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
