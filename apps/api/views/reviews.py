"""Reviews API Views"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from apps.reviews.models import Review
from apps.api.serializers.reviews import ReviewSerializer, ReviewCreateSerializer
from apps.api.pagination import StandardResultsSetPagination
from apps.api.permissions import IsOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """Review ViewSet for public API"""
    queryset = Review.objects.filter(is_approved=True).select_related('user', 'business').order_by('-created_at')
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['business', 'rating', 'is_approved']
    search_fields = ['comment', 'user__username', 'business__name_ar', 'business__name_en']
    ordering_fields = ['created_at', 'rating']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # If user is authenticated, show their reviews even if not approved
        if self.request.user.is_authenticated:
            queryset = Review.objects.filter(
                is_approved=True
            ).select_related('user', 'business') | Review.objects.filter(
                user=self.request.user
            ).select_related('user', 'business')
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like a review"""
        review = self.get_object()
        # Implement like logic here
        return Response({'status': 'liked'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def report(self, request, pk=None):
        """Report a review"""
        review = self.get_object()
        reason = request.data.get('reason', '')
        # Implement report logic here
        return Response({'status': 'reported'})