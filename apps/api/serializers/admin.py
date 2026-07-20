"""Admin Dashboard API Serializers"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

# Import models from their respective apps
from apps.directory.models import Business, Category
from apps.products.models import Product
from apps.deals.models import Deal
from apps.reviews.models import Review

User = get_user_model()


class DashboardStatsSerializer(serializers.Serializer):
    """Dashboard statistics"""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    new_users_week = serializers.IntegerField()
    staff_users = serializers.IntegerField()
    
    total_businesses = serializers.IntegerField()
    verified_businesses = serializers.IntegerField()
    pending_verification = serializers.IntegerField()
    featured_businesses = serializers.IntegerField()
    
    total_products = serializers.IntegerField()
    active_products = serializers.IntegerField()
    
    total_deals = serializers.IntegerField()
    active_deals = serializers.IntegerField()
    
    total_reviews = serializers.IntegerField()
    pending_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()
    
    total_views = serializers.IntegerField()
    total_clicks = serializers.IntegerField()


class AdminUserSerializer(serializers.ModelSerializer):
    """User serializer for admin"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    businesses_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login',
            'businesses_count', 'reviews_count'
        ]
    
    def get_businesses_count(self, obj) -> int:
        return obj.businesses.count()
    
    def get_reviews_count(self, obj) -> int:
        return obj.reviews.count()


class AdminBusinessSerializer(serializers.ModelSerializer):
    """Business serializer for admin"""
    owner = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    business_type_display = serializers.CharField(source='get_business_type_display', read_only=True)
    
    class Meta:
        model = Business
        fields = '__all__'


class AdminCategorySerializer(serializers.ModelSerializer):
    """Category serializer for admin"""
    businesses_count = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name_ar', read_only=True, allow_null=True)
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_businesses_count(self, obj) -> int:
        return obj.business_set.count()


class AdminProductSerializer(serializers.ModelSerializer):
    """Product serializer for admin"""
    business = serializers.StringRelatedField()
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class AdminDealSerializer(serializers.ModelSerializer):
    """Deal serializer for admin"""
    business = serializers.StringRelatedField()
    deal_type_display = serializers.CharField(source='get_deal_type_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Deal
        fields = '__all__'
    
    def get_days_remaining(self, obj) -> int | None:
        if obj.end_date:
            delta = obj.end_date - timezone.now().date()
            return delta.days if delta.days > 0 else 0
        return None


class AdminReviewSerializer(serializers.ModelSerializer):
    """Review serializer for admin"""
    user = serializers.StringRelatedField()
    business = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = '__all__'


class AdminAnalyticsSerializer(serializers.Serializer):
    """Analytics data"""
    period = serializers.CharField()
    users = serializers.IntegerField()
    businesses = serializers.IntegerField()
    products = serializers.IntegerField()
    reviews = serializers.IntegerField()
    views = serializers.IntegerField()
    clicks = serializers.IntegerField()
