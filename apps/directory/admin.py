"""
Directory Admin Configuration
==============================
إعدادات Django Admin لجميع نماذج Directory
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    Governorate,
    City,
    District,
    Business,
    BusinessImage,
    Favorite
)


# ========================================
# Governorate Admin
# ========================================
@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    list_display = [
        'name_en',
        'name_ar',
        'order',
        'is_active',
        'cities_count',
        'businesses_count',
        'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_en', 'name_ar']
    prepopulated_fields = {'slug': ('name_en',)}
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name_en']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name_en', 'name_ar', 'slug')
        }),
        (_('Description'), {
            'fields': ('description_en', 'description_ar')
        }),
        (_('Media'), {
            'fields': ('icon', 'image')
        }),
        (_('Settings'), {
            'fields': ('is_active', 'order')
        }),
    )
    
    def cities_count(self, obj):
        return obj.get_cities_count()
    cities_count.short_description = 'Cities'
    
    def businesses_count(self, obj):
        return obj.get_business_count()
    businesses_count.short_description = 'Businesses'


# ========================================
# City Admin
# ========================================
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = [
        'name_en',
        'name_ar',
        'governorate',
        'order',
        'is_active',
        'districts_count',
        'businesses_count'
    ]
    list_filter = ['governorate', 'is_active']
    search_fields = ['name_en', 'name_ar', 'governorate__name_en']
    prepopulated_fields = {'slug': ('name_en',)}
    list_editable = ['order', 'is_active']
    autocomplete_fields = ['governorate']
    
    def districts_count(self, obj):
        return obj.get_districts_count()
    districts_count.short_description = 'Districts'
    
    def businesses_count(self, obj):
        return obj.get_business_count()
    businesses_count.short_description = 'Businesses'


# ========================================
# District Admin
# ========================================
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = [
        'name_en',
        'name_ar',
        'city',
        'governorate',
        'order',
        'is_active',
        'businesses_count'
    ]
    list_filter = ['city__governorate', 'city', 'is_active']
    search_fields = ['name_en', 'name_ar', 'city__name_en']
    prepopulated_fields = {'slug': ('name_en',)}
    list_editable = ['order', 'is_active']
    autocomplete_fields = ['city']
    
    def governorate(self, obj):
        return obj.governorate
    governorate.short_description = 'Governorate'
    
    def businesses_count(self, obj):
        return obj.get_business_count()
    businesses_count.short_description = 'Businesses'


# ========================================
# Business Image Inline
# ========================================
class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 1
    fields = ['image', 'caption_en', 'caption_ar', 'order', 'is_active']


# ========================================
# Business Admin
# ========================================
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'name_en',
        'business_type_badge',
        'category',
        'district',
        'owner',
        'status_badges',
        'rating_display',
        'view_count',
        'created_at'
    ]
    list_filter = [
        'business_type',
        'is_active',
        'is_verified',
        'is_featured',
        'is_promoted',
        'category',
        'district__city__governorate',
        'created_at'
    ]
    search_fields = [
        'name_en',
        'name_ar',
        'owner__email',
        'phone',
        'email'
    ]
    prepopulated_fields = {'slug': ('name_en',)}
    autocomplete_fields = ['category', 'district', 'owner']
    inlines = [BusinessImageInline]
    
    readonly_fields = [
        'view_count',
        'click_count',
        'created_at',
        'updated_at',
        'verified_at'
    ]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'owner',
                'business_type',
                'name_en',
                'name_ar',
                'slug',
                'category',
                'district'
            )
        }),
        (_('Images'), {
            'fields': ('logo', 'cover_image')
        }),
        (_('Contact Information'), {
            'fields': (
                'phone',
                'whatsapp',
                'email',
                'website'
            )
        }),
        (_('Social Media'), {
            'fields': ('facebook', 'instagram', 'twitter', 'tiktok'),
            'classes': ('collapse',)
        }),
        (_('Location'), {
            'fields': (
                'address_en',
                'address_ar',
                'location_url',
                'latitude',
                'longitude'
            )
        }),
        (_('Description'), {
            'fields': (
                'description_en',
                'description_ar',
                'working_hours_en',
                'working_hours_ar'
            )
        }),
        (_('Status'), {
            'fields': (
                'is_active',
                'is_verified',
                'is_featured',
                'is_promoted'
            )
        }),
        (_('Statistics'), {
            'fields': (
                'view_count',
                'click_count',
                'created_at',
                'updated_at',
                'verified_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def business_type_badge(self, obj):
        """Display business type with icon"""
        colors = {
            'shop': '#3498db',
            'craft': '#e67e22',
            'public': '#2ecc71',
        }
        icons = {
            'shop': '🏪',
            'craft': '🔧',
            'public': '🏛️',
        }
        type_name = obj.get_business_type_display()
        color = colors.get(obj.business_type, '#95a5a6')
        icon = icons.get(obj.business_type, '📍')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color,
            icon,
            type_name
        )
    business_type_badge.short_description = 'نوع المحل / Type'
    
    def status_badges(self, obj):
        badges = []
        if obj.is_active:
            badges.append('<span style="color: green;">✓ Active</span>')
        if obj.is_verified:
            badges.append('<span style="color: blue;">✓ Verified</span>')
        if obj.is_featured:
            badges.append('<span style="color: orange;">⭐ Featured</span>')
        if obj.is_promoted:
            badges.append('<span style="color: purple;">🚀 Promoted</span>')
        return format_html(' | '.join(badges)) if badges else '-'
    status_badges.short_description = 'Status'
    
    def rating_display(self, obj):
        rating = obj.average_rating
        reviews = obj.total_reviews
        if rating > 0:
            stars = '⭐' * int(rating)
            return format_html(
                '{} <small>({:.1f} / {})</small>',
                stars,
                rating,
                reviews
            )
        return '-'
    rating_display.short_description = 'Rating'
    
    actions = ['verify_businesses', 'feature_businesses', 'activate_businesses']
    
    def verify_businesses(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} businesses verified.")
    verify_businesses.short_description = "Verify selected businesses"
    
    def feature_businesses(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} businesses featured.")
    feature_businesses.short_description = "Feature selected businesses"
    
    def activate_businesses(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} businesses activated.")
    activate_businesses.short_description = "Activate selected businesses"


# ========================================
# Business Image Admin
# ========================================
@admin.register(BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ['business', 'caption_en', 'order', 'is_active', 'uploaded_at']
    list_filter = ['is_active', 'uploaded_at']
    search_fields = ['business__name_en', 'caption_en', 'caption_ar']
    list_editable = ['order', 'is_active']
    autocomplete_fields = ['business']


# ========================================
# Favorite Admin
# ========================================
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'business__name_en']
    autocomplete_fields = ['user', 'business']
    date_hierarchy = 'created_at'
