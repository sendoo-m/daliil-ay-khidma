"""Business Owner API Views"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg
from django.utils import timezone

# Import models from their respective apps
from apps.directory.models import Business
from apps.products.models import Product
from apps.deals.models import Deal
from apps.reviews.models import Review

from apps.api.serializers.business_owner import (
    BusinessOwnerStatsSerializer,
    BusinessOwnerBusinessSerializer,
    BusinessOwnerProductSerializer,
    BusinessOwnerDealSerializer,
    BusinessOwnerReviewSerializer
)
from apps.api.permissions import IsBusinessOwner
from apps.api.pagination import StandardResultsPagination


class BusinessOwnerDashboardViewSet(viewsets.ViewSet):
    """Business owner dashboard"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get business owner stats"""
        user = request.user
        businesses = Business.objects.filter(owner=user)
        
        stats = {
            'total_businesses': businesses.count(),
            'verified_businesses': businesses.filter(is_verified=True).count(),
            'total_products': Product.objects.filter(business__owner=user).count(),
            'total_deals': Deal.objects.filter(business__owner=user).count(),
            'active_deals': Deal.objects.filter(
                business__owner=user,
                is_active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).count(),
            'total_reviews': Review.objects.filter(business__owner=user, is_approved=True).count(),
            'average_rating': Review.objects.filter(
                business__owner=user, 
                is_approved=True
            ).aggregate(Avg('rating'))['rating__avg'] or 0,
            'total_views': businesses.aggregate(Sum('views_count'))['views_count__sum'] or 0,
            'total_clicks': businesses.aggregate(Sum('clicks_count'))['clicks_count__sum'] or 0,
        }
        
        serializer = BusinessOwnerStatsSerializer(stats)
        return Response(serializer.data)


class BusinessOwnerBusinessViewSet(viewsets.ModelViewSet):
    """Business owner business management"""
    serializer_class = BusinessOwnerBusinessSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user).select_related('category')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BusinessOwnerProductViewSet(viewsets.ModelViewSet):
    """Business owner product management"""
    serializer_class = BusinessOwnerProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        business_id = self.kwargs.get('business_pk')
        return Product.objects.filter(
            business_id=business_id,
            business__owner=self.request.user
        ).select_related('business')
    
    def perform_create(self, serializer):
        business_id = self.kwargs.get('business_pk')
        business = Business.objects.get(id=business_id, owner=self.request.user)
        serializer.save(business=business)


class BusinessOwnerDealViewSet(viewsets.ModelViewSet):
    """Business owner deal management"""
    serializer_class = BusinessOwnerDealSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        business_id = self.kwargs.get('business_pk')
        return Deal.objects.filter(
            business_id=business_id,
            business__owner=self.request.user
        ).select_related('business')
    
    def perform_create(self, serializer):
        business_id = self.kwargs.get('business_pk')
        business = Business.objects.get(id=business_id, owner=self.request.user)
        serializer.save(business=business)


class BusinessOwnerReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """Business owner review viewing"""
    serializer_class = BusinessOwnerReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        business_id = self.kwargs.get('business_pk')
        return Review.objects.filter(
            business_id=business_id,
            business__owner=self.request.user
        ).select_related('user', 'business').order_by('-created_at')