"""Admin Dashboard API Views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta

from apps.directory.models import Business, Category
from apps.products.models import Product
from apps.deals.models import Deal
from apps.reviews.models import Review

from apps.api.serializers.admin import (
    DashboardStatsSerializer, AdminUserSerializer,
    AdminBusinessSerializer, AdminCategorySerializer,
    AdminProductSerializer, AdminDealSerializer,
    AdminReviewSerializer, AdminAnalyticsSerializer
)
from apps.api.permissions import IsAdminUser
from apps.api.pagination import StandardResultsSetPagination

User = get_user_model()


class AdminDashboardViewSet(viewsets.ViewSet):
    """Admin dashboard statistics"""
    permission_classes = [IsAdminUser]
    serializer_class = DashboardStatsSerializer

    def get_serializer_class(self):
        if self.action == 'analytics':
            return AdminAnalyticsSerializer
        return DashboardStatsSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        one_week_ago = timezone.now() - timedelta(days=7)

        stats = {
            'total_users':          User.objects.count(),
            'active_users':         User.objects.filter(is_active=True).count(),
            'new_users_week':       User.objects.filter(date_joined__gte=one_week_ago).count(),
            'staff_users':          User.objects.filter(is_staff=True).count(),
            'total_businesses':     Business.objects.count(),
            'verified_businesses':  Business.objects.filter(is_verified=True).count(),
            'pending_verification': Business.objects.filter(is_verified=False, is_active=True).count(),
            'featured_businesses':  Business.objects.filter(is_featured=True).count(),
            'total_products':       Product.objects.count(),
            'active_products':      Product.objects.filter(is_available=True).count(),
            'total_deals':          Deal.objects.count(),
            'active_deals':         Deal.objects.filter(
                is_active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).count(),
            'total_reviews':        Review.objects.count(),
            'pending_reviews':      Review.objects.filter(is_approved=False).count(),
            'average_rating':       Review.objects.filter(is_approved=True).aggregate(
                Avg('rating'))['rating__avg'] or 0,
            'total_views':          Business.objects.aggregate(Sum('view_count'))['view_count__sum'] or 0,
            'total_clicks':         Business.objects.aggregate(Sum('click_count'))['click_count__sum'] or 0,
        }

        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Analytics data — مقسمة بالشهر للسنة الحالية فقط"""
        # ✅ مضاف فلتر السنة الحالية
        current_year = timezone.now().year
        MONTHS_AR = ['يناير','فبراير','مارس','أبريل','مايو','يونيو',
                     'يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر']

        data = []
        for month in range(1, 13):
            data.append({
                'period':     MONTHS_AR[month - 1],
                'users':      User.objects.filter(date_joined__year=current_year, date_joined__month=month).count(),
                'businesses': Business.objects.filter(created_at__year=current_year, created_at__month=month).count(),
                'products':   Product.objects.filter(created_at__year=current_year, created_at__month=month).count(),
                'reviews':    Review.objects.filter(created_at__year=current_year, created_at__month=month).count(),
                'views':      0,
                'clicks':     0,
            })

        serializer = AdminAnalyticsSerializer(data, many=True)
        return Response(serializer.data)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username', 'email']

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({'status': 'success', 'is_active': user.is_active})

    @action(detail=True, methods=['post'])
    def make_staff(self, request, pk=None):
        user = self.get_object()
        user.is_staff = True
        user.save()
        return Response({'status': 'success'})


class AdminBusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all().select_related('owner', 'category').order_by('-created_at')
    serializer_class = AdminBusinessSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['is_active', 'is_verified', 'is_featured', 'business_type', 'category']
    search_fields = ['name_ar', 'name_en', 'owner__username']
    ordering_fields = ['created_at', 'views_count', 'clicks_count']

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        business = self.get_object()
        business.is_verified = True
        business.save()
        return Response({'status': 'success'})

    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        business = self.get_object()
        business.is_featured = not business.is_featured
        business.save()
        return Response({'status': 'success', 'is_featured': business.is_featured})


class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('order', 'name_ar')
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['is_active', 'parent']
    search_fields = ['name_ar', 'name_en']
    ordering_fields = ['order', 'name_ar']


class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('business').order_by('-created_at')
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['is_available', 'is_featured', 'product_type', 'business']
    search_fields = ['name_ar', 'name_en', 'business__name_ar']
    ordering_fields = ['created_at', 'price']


class AdminDealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all().select_related('business').order_by('-created_at')
    serializer_class = AdminDealSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['is_active', 'is_featured', 'deal_type', 'business']
    search_fields = ['title_ar', 'title_en', 'business__name_ar']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'used_count']


class AdminReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('user', 'business').order_by('-created_at')
    serializer_class = AdminReviewSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['is_approved', 'rating', 'business']
    search_fields = ['user__username', 'business__name_ar', 'comment']
    ordering_fields = ['created_at', 'rating']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        review = self.get_object()
        review.is_approved = True
        review.approved_by = request.user
        review.approved_at = timezone.now()
        review.save()
        return Response({'status': 'success'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        review = self.get_object()
        review.is_approved = False
        review.save()
        return Response({'status': 'success'})

# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.contrib.auth import get_user_model
# from django.db.models import Count, Sum, Avg, Q
# from django.utils import timezone
# from datetime import timedelta

# # Import models from their respective apps
# from apps.directory.models import Business, Category
# from apps.products.models import Product
# from apps.deals.models import Deal
# from apps.reviews.models import Review

# from apps.api.serializers.admin import (
#     DashboardStatsSerializer,
#     AdminUserSerializer,
#     AdminBusinessSerializer,
#     AdminCategorySerializer,
#     AdminProductSerializer,
#     AdminDealSerializer,
#     AdminReviewSerializer,
#     AdminAnalyticsSerializer
# )
# from apps.api.permissions import IsAdminUser
# from apps.api.pagination import StandardResultsSetPagination

# User = get_user_model()


# class AdminDashboardViewSet(viewsets.ViewSet):
#     """Admin dashboard statistics"""
#     permission_classes = [IsAdminUser]
    
#     @action(detail=False, methods=['get'])
#     def stats(self, request):
#         """Get dashboard statistics"""
#         one_week_ago = timezone.now() - timedelta(days=7)
        
#         stats = {
#             # Users
#             'total_users': User.objects.count(),
#             'active_users': User.objects.filter(is_active=True).count(),
#             'new_users_week': User.objects.filter(date_joined__gte=one_week_ago).count(),
#             'staff_users': User.objects.filter(is_staff=True).count(),
            
#             # Businesses
#             'total_businesses': Business.objects.count(),
#             'verified_businesses': Business.objects.filter(is_verified=True).count(),
#             'pending_verification': Business.objects.filter(is_verified=False, is_active=True).count(),
#             'featured_businesses': Business.objects.filter(is_featured=True).count(),
            
#             # Products
#             'total_products': Product.objects.count(),
#             'active_products': Product.objects.filter(is_available=True).count(),
            
#             # Deals
#             'total_deals': Deal.objects.count(),
#             'active_deals': Deal.objects.filter(
#                 is_active=True,
#                 start_date__lte=timezone.now(),
#                 end_date__gte=timezone.now()
#             ).count(),
            
#             # Reviews
#             'total_reviews': Review.objects.count(),
#             'pending_reviews': Review.objects.filter(is_approved=False).count(),
#             'average_rating': Review.objects.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 0,
            
#             # Analytics
#             'total_views': Business.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0,
#             'total_clicks': Business.objects.aggregate(Sum('clicks_count'))['clicks_count__sum'] or 0,
#         }
        
#         serializer = DashboardStatsSerializer(stats)
#         return Response(serializer.data)
    
#     @action(detail=False, methods=['get'])
#     def analytics(self, request):
#         """Get analytics data for charts"""
#         period = request.query_params.get('period', 'monthly')  # daily, weekly, monthly
        
#         # This is a simplified version - you can expand based on your needs
#         data = []
#         for i in range(6):
#             data.append({
#                 'period': f'Period {i+1}',
#                 'users': User.objects.filter(date_joined__month=i+1).count(),
#                 'businesses': Business.objects.filter(created_at__month=i+1).count(),
#                 'products': Product.objects.filter(created_at__month=i+1).count(),
#                 'reviews': Review.objects.filter(created_at__month=i+1).count(),
#                 'views': 0,  # Calculate actual views
#                 'clicks': 0,  # Calculate actual clicks
#             })
        
#         serializer = AdminAnalyticsSerializer(data, many=True)
#         return Response(serializer.data)


# class AdminUserViewSet(viewsets.ModelViewSet):
#     """Admin user management"""
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = AdminUserSerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['is_active', 'is_staff', 'is_superuser']
#     search_fields = ['username', 'email', 'first_name', 'last_name']
#     ordering_fields = ['date_joined', 'username', 'email']
    
#     @action(detail=True, methods=['post'])
#     def toggle_active(self, request, pk=None):
#         """Toggle user active status"""
#         user = self.get_object()
#         user.is_active = not user.is_active
#         user.save()
#         return Response({'status': 'success', 'is_active': user.is_active})
    
#     @action(detail=True, methods=['post'])
#     def make_staff(self, request, pk=None):
#         """Make user staff"""
#         user = self.get_object()
#         user.is_staff = True
#         user.save()
#         return Response({'status': 'success'})


# class AdminBusinessViewSet(viewsets.ModelViewSet):
#     """Admin business management"""
#     queryset = Business.objects.all().select_related('owner', 'category').order_by('-created_at')
#     serializer_class = AdminBusinessSerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['is_active', 'is_verified', 'is_featured', 'business_type', 'category']
#     search_fields = ['name_ar', 'name_en', 'owner__username']
#     ordering_fields = ['created_at', 'views_count', 'clicks_count']
    
#     @action(detail=True, methods=['post'])
#     def verify(self, request, pk=None):
#         """Verify business"""
#         business = self.get_object()
#         business.is_verified = True
#         business.save()
#         return Response({'status': 'success'})
    
#     @action(detail=True, methods=['post'])
#     def toggle_featured(self, request, pk=None):
#         """Toggle featured status"""
#         business = self.get_object()
#         business.is_featured = not business.is_featured
#         business.save()
#         return Response({'status': 'success', 'is_featured': business.is_featured})


# class AdminCategoryViewSet(viewsets.ModelViewSet):
#     """Admin category management"""
#     queryset = Category.objects.all().order_by('order', 'name_ar')
#     serializer_class = AdminCategorySerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['is_active', 'parent']
#     search_fields = ['name_ar', 'name_en']
#     ordering_fields = ['order', 'name_ar']


# class AdminProductViewSet(viewsets.ModelViewSet):
#     """Admin product management"""
#     queryset = Product.objects.all().select_related('business').order_by('-created_at')
#     serializer_class = AdminProductSerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['is_available', 'is_featured', 'product_type', 'business']
#     search_fields = ['name_ar', 'name_en', 'business__name_ar']
#     ordering_fields = ['created_at', 'price']


# class AdminDealViewSet(viewsets.ModelViewSet):
#     """Admin deal management"""
#     queryset = Deal.objects.all().select_related('business').order_by('-created_at')
#     serializer_class = AdminDealSerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['is_active', 'is_featured', 'deal_type', 'business']
#     search_fields = ['title_ar', 'title_en', 'business__name_ar']
#     ordering_fields = ['created_at', 'start_date', 'end_date', 'used_count']


# class AdminReviewViewSet(viewsets.ModelViewSet):
#     """Admin review management"""
#     queryset = Review.objects.all().select_related('user', 'business').order_by('-created_at')
#     serializer_class = AdminReviewSerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['is_approved', 'rating', 'business']
#     search_fields = ['user__username', 'business__name_ar', 'comment']
#     ordering_fields = ['created_at', 'rating']
    
#     @action(detail=True, methods=['post'])
#     def approve(self, request, pk=None):
#         """Approve review"""
#         review = self.get_object()
#         review.is_approved = True
#         review.approved_by = request.user
#         review.approved_at = timezone.now()
#         review.save()
#         return Response({'status': 'success'})
    
#     @action(detail=True, methods=['post'])
#     def reject(self, request, pk=None):
#         """Reject review"""
#         review = self.get_object()
#         review.is_approved = False
#         review.save()
#         return Response({'status': 'success'})
