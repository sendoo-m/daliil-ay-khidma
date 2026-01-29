from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Deal, DealClaim


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        'title_en',
        'business',
        'deal_type',
        'status_badge',
        'discount_display',
        'validity_period',
        'uses_display',
        'is_featured',
        'view_count'
    )
    
    list_filter = (
        'deal_type',
        'is_active',
        'is_featured',
        'start_date',
        'end_date',
        'created_at'
    )
    
    search_fields = (
        'title_en',
        'title_ar',
        'description_en',
        'description_ar',
        'business__name_en',
        'business__name_ar'
    )
    
    readonly_fields = (
        'slug',
        'current_uses',
        'view_count',
        'created_at',
        'updated_at'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'business',
                'title_en',
                'title_ar',
                'slug',
                'description_en',
                'description_ar'
            )
        }),
        ('Deal Details', {
            'fields': (
                'deal_type',
                'discount_percentage',
                'discount_amount',
                'original_price',
                'final_price'
            )
        }),
        ('Validity', {
            'fields': (
                'start_date',
                'end_date'
            )
        }),
        ('Terms & Conditions', {
            'fields': (
                'terms_en',
                'terms_ar'
            )
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Limits', {
            'fields': (
                'max_uses',
                'current_uses',
                'max_uses_per_user'
            )
        }),
        ('Display Settings', {
            'fields': (
                'is_active',
                'is_featured',
                'order'
            )
        }),
        ('Statistics', {
            'fields': (
                'view_count',
                'created_at',
                'updated_at'
            )
        }),
    )
    
    def status_badge(self, obj):
        now = timezone.now()
        if obj.is_expired:
            return format_html(
                '<span style="background: #dc3545; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">Expired</span>'
            )
        elif obj.is_upcoming:
            return format_html(
                '<span style="background: #17a2b8; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">Upcoming</span>'
            )
        elif obj.is_valid:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">Active</span>'
            )
        else:
            return format_html(
                '<span style="background: #6c757d; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">Inactive</span>'
            )
    status_badge.short_description = 'Status'
    
    def discount_display(self, obj):
        if obj.deal_type == 'percentage' and obj.discount_percentage:
            return f"{obj.discount_percentage}%"
        elif obj.deal_type == 'fixed' and obj.discount_amount:
            return f"{obj.discount_amount} EGP"
        else:
            return '-'
    discount_display.short_description = 'Discount'
    
    def validity_period(self, obj):
        return f"{obj.start_date.strftime('%Y-%m-%d')} → {obj.end_date.strftime('%Y-%m-%d')}"
    validity_period.short_description = 'Validity'
    
    def uses_display(self, obj):
        if obj.max_uses:
            return f"{obj.current_uses}/{obj.max_uses}"
        return f"{obj.current_uses}/∞"
    uses_display.short_description = 'Uses'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business')


@admin.register(DealClaim)
class DealClaimAdmin(admin.ModelAdmin):
    list_display = (
        'deal',
        'user',
        'claimed_at',
        'is_used',
        'used_at'
    )
    
    list_filter = (
        'is_used',
        'claimed_at',
        'used_at'
    )
    
    search_fields = (
        'deal__title_en',
        'deal__title_ar',
        'user__username',
        'user__email'
    )
    
    readonly_fields = ('claimed_at', 'used_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'deal',
            'user'
        )
