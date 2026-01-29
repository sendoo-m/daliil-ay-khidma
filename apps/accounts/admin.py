"""
User Admin Configuration
========================
إعدادات Django Admin للمستخدمين
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """إدارة المستخدمين في Admin"""
    
    list_display = [
        'username',
        'email',
        'phone',
        'full_name',
        'profile_image',
        'account_type',
        'email_status',
        'is_active',
        'date_joined',
    ]
    
    list_filter = [
        'is_business_owner',
        'email_verified',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    ]
    
    search_fields = [
        'username',
        'email',
        'phone',
        'first_name',
        'last_name',
    ]
    
    ordering = ['-date_joined']
    
    readonly_fields = [
        'date_joined',
        'last_login',
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'profile_picture',
                'bio',
                'city',
            )
        }),
        (_('Account Type'), {
            'fields': (
                'is_business_owner',
                'email_verified',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone',
                'password1',
                'password2',
                'is_business_owner',
            ),
        }),
    )
    
    # Custom Display Methods
    def profile_image(self, obj):
        """عرض الصورة الشخصية"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="40" height="40" '
                'style="border-radius: 50%; object-fit: cover;" />',
                obj.get_profile_picture_url()
            )
        return format_html(
            '<div style="width: 40px; height: 40px; background: #ddd; '
            'border-radius: 50%; display: flex; align-items: center; '
            'justify-content: center; color: #666;">{}</div>',
            obj.username[0].upper()
        )
    profile_image.short_description = 'الصورة'
    
    def account_type(self, obj):
        """عرض نوع الحساب"""
        if obj.is_superuser:
            return format_html(
                '<span style="background: #d32f2f; color: white; '
                'padding: 3px 8px; border-radius: 3px; font-size: 11px;">🔑 Superuser</span>'
            )
        elif obj.is_staff:
            return format_html(
                '<span style="background: #f57c00; color: white; '
                'padding: 3px 8px; border-radius: 3px; font-size: 11px;">⚙️ Admin</span>'
            )
        elif obj.is_business_owner:
            return format_html(
                '<span style="background: #1976d2; color: white; '
                'padding: 3px 8px; border-radius: 3px; font-size: 11px;">🏪 Owner</span>'
            )
        return format_html(
            '<span style="background: #388e3c; color: white; '
            'padding: 3px 8px; border-radius: 3px; font-size: 11px;">👤 User</span>'
        )
    account_type.short_description = 'نوع الحساب'
    
    def email_status(self, obj):
        """حالة البريد الإلكتروني"""
        if obj.email_verified:
            return format_html(
                '<span style="color: green;">✓ مفعّل</span>'
            )
        return format_html(
            '<span style="color: orange;">⚠ غير مفعّل</span>'
        )
    email_status.short_description = 'حالة البريد'
    
    # Actions
    actions = ['verify_emails', 'make_business_owner', 'activate_users']
    
    def verify_emails(self, request, queryset):
        """تفعيل البريد الإلكتروني"""
        updated = queryset.update(email_verified=True)
        self.message_user(request, f"تم تفعيل {updated} بريد إلكتروني.")
    verify_emails.short_description = "تفعيل البريد الإلكتروني"
    
    def make_business_owner(self, request, queryset):
        """تحويل لصاحب محل"""
        updated = queryset.update(is_business_owner=True)
        self.message_user(request, f"تم تحويل {updated} مستخدم لصاحب محل.")
    make_business_owner.short_description = "تحويل لصاحب محل"
    
    def activate_users(self, request, queryset):
        """تفعيل المستخدمين"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"تم تفعيل {updated} مستخدم.")
    activate_users.short_description = "تفعيل المستخدمين"
