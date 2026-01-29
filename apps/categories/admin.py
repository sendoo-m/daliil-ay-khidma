"""
Category Admin Configuration
============================
إعدادات Django Admin للتصنيفات
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from apps.directory.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """إدارة التصنيفات في Admin"""
    
    list_display = [
        'icon_display',
        'name_en',
        'name_ar',
        'parent',
        'business_count',
        'order_badge',
        'status_badge',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'parent',
        'created_at',
    ]
    
    search_fields = [
        'name_en',
        'name_ar',
        'slug',
        'description_en',
        'description_ar',
    ]
    
    list_editable = ['order']
    
    readonly_fields = [
        'slug',
        'created_at',
        'updated_at',
        'image_preview',
    ]
    
    fieldsets = (
        (None, {
            'fields': (
                'parent',
                'is_active',
            )
        }),
        (_('Names'), {
            'fields': (
                'name_en',
                'name_ar',
                'slug',
            )
        }),
        (_('Descriptions'), {
            'fields': (
                'description_en',
                'description_ar',
            ),
            'classes': ('collapse',)
        }),
        (_('Visual'), {
            'fields': (
                'icon',
                'image',
                'image_preview',
                'order',
            )
        }),
        (_('SEO'), {
            'fields': (
                'meta_keywords_en',
                'meta_keywords_ar',
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    prepopulated_fields = {}
    
    ordering = ['order', 'name_en']
    
    # Custom Display Methods
    def icon_display(self, obj):
        """عرض الأيقونة"""
        if obj.icon:
            return format_html(
                '<i class="{}" style="font-size: 20px; color: #1976d2;"></i>',
                obj.icon
            )
        return '-'
    icon_display.short_description = 'الأيقونة'
    
    def business_count(self, obj):
        """عدد المحلات"""
        count = obj.get_business_count()
        total = obj.get_all_business_count()
        if total > count:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span> '
                '<span style="color: gray;">({} مع الفرعية)</span>',
                count, total
            )
        return format_html(
            '<span style="color: green; font-weight: bold;">{}</span>',
            count
        )
    business_count.short_description = 'عدد المحلات'
    
    def order_badge(self, obj):
        """ترتيب العرض"""
        return format_html(
            '<span style="background: #e3f2fd; color: #1976d2; '
            'padding: 4px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            obj.order
        )
    order_badge.short_description = 'الترتيب'
    
    def status_badge(self, obj):
        """حالة التفعيل"""
        if obj.is_active:
            return format_html(
                '<span style="background: #c8e6c9; color: #2e7d32; '
                'padding: 4px 10px; border-radius: 12px; font-size: 11px;">✓ نشط</span>'
            )
        return format_html(
            '<span style="background: #ffcdd2; color: #c62828; '
            'padding: 4px 10px; border-radius: 12px; font-size: 11px;">✕ غير نشط</span>'
        )
    status_badge.short_description = 'الحالة'
    
    def image_preview(self, obj):
        """معاينة الصورة"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; '
                'border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html(
            '<p style="color: #999; font-style: italic;">لا توجد صورة</p>'
        )
    image_preview.short_description = 'معاينة الصورة'
    
    # Actions
    actions = ['activate_categories', 'deactivate_categories']
    
    def activate_categories(self, request, queryset):
        """تفعيل التصنيفات"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"تم تفعيل {updated} تصنيف.")
    activate_categories.short_description = "تفعيل التصنيفات المحددة"
    
    def deactivate_categories(self, request, queryset):
        """تعطيل التصنيفات"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"تم تعطيل {updated} تصنيف.")
    deactivate_categories.short_description = "تعطيل التصنيفات المحددة"
