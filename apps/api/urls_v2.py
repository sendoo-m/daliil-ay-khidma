"""API v2 URLs - Complete API for mobile apps"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from apps.api.views.admin import (
    AdminDashboardViewSet,
    AdminUserViewSet,
    AdminBusinessViewSet,
    AdminCategoryViewSet,
    AdminProductViewSet,
    AdminDealViewSet,
    AdminReviewViewSet
)
from apps.api.views.business_owner import (
    BusinessOwnerDashboardViewSet,
    BusinessOwnerBusinessViewSet,
    BusinessOwnerProductViewSet,
    BusinessOwnerDealViewSet,
    BusinessOwnerReviewViewSet
)
from apps.api.views import directory, deals, products, reviews, subscriptions
from apps.api.views.auth import (
    CustomTokenObtainPairView,
    TokenRefreshView,
    register,
    get_user_profile,
    update_user_profile,
    change_password
)

app_name = 'api_v2'

# Main router
router = DefaultRouter()

# ==================== ADMIN APIs ====================
router.register(r'admin/dashboard', AdminDashboardViewSet, basename='admin-dashboard')
router.register(r'admin/users', AdminUserViewSet, basename='admin-users')
router.register(r'admin/businesses', AdminBusinessViewSet, basename='admin-businesses')
router.register(r'admin/categories', AdminCategoryViewSet, basename='admin-categories')
router.register(r'admin/products', AdminProductViewSet, basename='admin-products')
router.register(r'admin/deals', AdminDealViewSet, basename='admin-deals')
router.register(r'admin/reviews', AdminReviewViewSet, basename='admin-reviews')

# ==================== BUSINESS OWNER APIs ====================
router.register(r'business-owner/dashboard', BusinessOwnerDashboardViewSet, basename='business-owner-dashboard')
router.register(r'business-owner/businesses', BusinessOwnerBusinessViewSet, basename='business-owner-businesses')

# Nested routes for business owner
business_router = routers.NestedDefaultRouter(router, r'business-owner/businesses', lookup='business')
business_router.register(r'products', BusinessOwnerProductViewSet, basename='business-owner-products')
business_router.register(r'deals', BusinessOwnerDealViewSet, basename='business-owner-deals')
business_router.register(r'reviews', BusinessOwnerReviewViewSet, basename='business-owner-reviews')

# ==================== PUBLIC APIs (for mobile app users) ====================
router.register(r'categories', directory.CategoryViewSet, basename='categories')
router.register(r'businesses', directory.BusinessViewSet, basename='businesses')
router.register(r'products', products.ProductViewSet, basename='products')
router.register(r'deals', deals.DealViewSet, basename='deals')
router.register(r'reviews', reviews.ReviewViewSet, basename='reviews')
router.register(r'subscriptions', subscriptions.SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    # Authentication
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register, name='register'),
    path('auth/profile/', get_user_profile, name='profile'),
    path('auth/profile/update/', update_user_profile, name='profile_update'),
    path('auth/change-password/', change_password, name='change_password'),
    
    # Include all routers
    path('', include(router.urls)),
    path('', include(business_router.urls)),
]