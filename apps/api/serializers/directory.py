"""
Directory Serializers
=====================
Serializers for Location & Business models
"""

from rest_framework import serializers
from apps.directory.models import (
    Governorate, City, District, Category,
    Business, BusinessImage, Favorite
)


class GovernorateSerializer(serializers.ModelSerializer):
    """Governorate Serializer"""
    
    class Meta:
        model = Governorate
        fields = [
            'id', 'name_en', 'name_ar', 'slug',
            'description_en', 'description_ar',
            'icon', 'image', 'is_active', 'order'
        ]
        read_only_fields = ['slug']


class CitySerializer(serializers.ModelSerializer):
    """City Serializer"""
    governorate = GovernorateSerializer(read_only=True)
    governorate_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = City
        fields = [
            'id', 'governorate', 'governorate_id',
            'name_en', 'name_ar', 'slug',
            'description_en', 'description_ar',
            'is_active', 'order'
        ]
        read_only_fields = ['slug']


class DistrictSerializer(serializers.ModelSerializer):
    """District Serializer"""
    city = CitySerializer(read_only=True)
    city_id = serializers.IntegerField(write_only=True)
    governorate = serializers.SerializerMethodField()
    
    class Meta:
        model = District
        fields = [
            'id', 'city', 'city_id', 'governorate',
            'name_en', 'name_ar', 'slug',
            'description_en', 'description_ar',
            'is_active', 'order'
        ]
        read_only_fields = ['slug']
    
    def get_governorate(self, obj):
        return GovernorateSerializer(obj.governorate).data


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""
    business_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name_en', 'name_ar', 'slug',
            'description_en', 'description_ar',
            'icon', 'image', 'is_active', 'order',
            'business_count'
        ]
        read_only_fields = ['slug']
    
    def get_business_count(self, obj):
        return obj.businesses.filter(is_active=True, is_verified=True).count()


class BusinessImageSerializer(serializers.ModelSerializer):
    """Business Image Serializer"""
    
    class Meta:
        model = BusinessImage
        fields = [
            'id', 'image', 'caption_en', 'caption_ar',
            'order', 'is_active', 'uploaded_at'
        ]


class BusinessListSerializer(serializers.ModelSerializer):
    """Business List Serializer (minimal)"""
    category = CategorySerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name_en', 'name_ar', 'slug',
            'logo', 'category', 'district',
            'phone', 'average_rating', 'total_reviews',
            'is_verified', 'is_featured', 'view_count'
        ]


class BusinessDetailSerializer(serializers.ModelSerializer):
    """Business Detail Serializer (full)"""
    category = CategorySerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    images = BusinessImageSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    city = serializers.SerializerMethodField()
    governorate = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = ['slug', 'owner', 'view_count', 'click_count']
    
    def get_city(self, obj):
        return CitySerializer(obj.city).data
    
    def get_governorate(self, obj):
        return GovernorateSerializer(obj.governorate).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Favorite Serializer"""
    business = BusinessListSerializer(read_only=True)
    business_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'business', 'business_id', 'created_at']
        read_only_fields = ['created_at']
