"""
API URLs
========
Main API router with all endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .views.directory import (
    GovernorateViewSet, CityViewSet, DistrictViewSet,
    CategoryViewSet, BusinessViewSet, FavoriteViewSet
)
from .views.products import ProductViewSet
from .views.deals import DealViewSet, DealClaimViewSet
from .views.subscriptions import SubscriptionPlanViewSet, SubscriptionViewSet

app_name = 'api'

# Create router
router = DefaultRouter()

# Directory endpoints
router.register(r'governorates', GovernorateViewSet, basename='governorate')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

# Products endpoints
router.register(r'products', ProductViewSet, basename='product')

# Deals endpoints
router.register(r'deals', DealViewSet, basename='deal')
router.register(r'deal-claims', DealClaimViewSet, basename='deal-claim')

# Subscriptions endpoints
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    # API Router
    path('', include(router.urls)),
    
    # API Authentication
    path('auth/', include('rest_framework.urls')),
    
    # API Documentation
    path('docs/', include_docs_urls(title='Daliil Ay Khidma API')),
]
