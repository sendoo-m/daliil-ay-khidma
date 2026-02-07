"""
Main Dashboard Views - Enhanced Version
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta, datetime
from calendar import monthrange

from apps.directory.models import Business
from apps.products.models import Product
from apps.deals.models import Deal
from apps.reviews.models import Review


@login_required
def dashboard_home(request):
    """الصفحة الرئيسية للداش بورد - محسّنة"""
    user = request.user
    
    # Get user's businesses
    businesses = Business.objects.filter(owner=user)
    
    # Check if user has no data and show helpful message
    if businesses.count() == 0:
        messages.info(
            request,
            'لا توجد بيانات لهذا المستخدم. '
            'للاختبار ببيانات تجريبية، '
            'سجّل خروج ودخول بـ: ahmed_owner '
            '(كلمة المرور: test123)'
        )
    
    # Basic Statistics
    stats = {
        'total_businesses': businesses.count(),
        'active_businesses': businesses.filter(is_active=True).count(),
        'verified_businesses': businesses.filter(is_verified=True).count(),
        'featured_businesses': businesses.filter(is_featured=True).count(),
        
        'total_products': Product.objects.filter(business__owner=user).count(),
        'active_products': Product.objects.filter(
            business__owner=user, 
            is_available=True
        ).count(),
        'products_count': Product.objects.filter(
            business__owner=user,
            product_type='product'
        ).count(),
        'services_count': Product.objects.filter(
            business__owner=user,
            product_type='service'
        ).count(),
        
        'total_deals': Deal.objects.filter(business__owner=user).count(),
        'active_deals': Deal.objects.filter(
            business__owner=user,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).count(),
        
        'total_views': businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0,
        'total_clicks': businesses.aggregate(Sum('click_count'))['click_count__sum'] or 0,
        
        'total_reviews': Review.objects.filter(business__owner=user).count(),
        'average_rating': Review.objects.filter(
            business__owner=user,
            is_approved=True
        ).aggregate(Avg('rating'))['rating__avg'] or 0,
    }
    
    # Business Type Distribution
    business_types = businesses.values('business_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Monthly Trends (last 6 months)
    monthly_data = []
    today = timezone.now()
    
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        _, last_day = monthrange(month_start.year, month_start.month)
        month_end = month_start.replace(day=last_day, hour=23, minute=59, second=59)
        
        month_businesses = businesses.filter(
            created_at__range=[month_start, month_end]
        )
        
        monthly_data.append({
            'month': month_start.strftime('%B'),
            'month_ar': get_arabic_month(month_start.month),
            'views': month_businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0,
            'clicks': month_businesses.aggregate(Sum('click_count'))['click_count__sum'] or 0,
        })
    
    # Recent businesses - FIXED: Use 'district' instead of 'governorate', 'city'
    recent_businesses = businesses.select_related(
        'category', 'district'
    ).order_by('-created_at')[:5]
    
    # Recent products
    recent_products = Product.objects.filter(
        business__owner=user
    ).select_related('business').order_by('-created_at')[:5]
    
    # Active deals
    active_deals = Deal.objects.filter(
        business__owner=user,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).select_related('business').order_by('-created_at')[:6]
    
    # Recent reviews
    recent_reviews = Review.objects.filter(
        business__owner=user
    ).select_related('business', 'user').order_by('-created_at')[:5]
    
    # Demo accounts info
    demo_accounts = [
        {'username': 'ahmed_owner', 'name': 'أحمد محمد', 'businesses': 2},
        {'username': 'fatima_owner', 'name': 'فاطمة علي', 'businesses': 2},
        {'username': 'khaled_owner', 'name': 'خالد حسن', 'businesses': 2},
        {'username': 'maha_owner', 'name': 'مها عبدالله', 'businesses': 2},
        {'username': 'omar_owner', 'name': 'عمر سعيد', 'businesses': 2},
    ]
    
    context = {
        'stats': stats,
        'business_types': business_types,
        'monthly_data': monthly_data,
        'recent_businesses': recent_businesses,
        'recent_products': recent_products,
        'active_deals': active_deals,
        'recent_reviews': recent_reviews,
        'has_data': businesses.count() > 0,
        'demo_accounts': demo_accounts,
    }
    
    return render(request, 'dashboard/home.html', context)


def get_arabic_month(month_number):
    """تحويل رقم الشهر إلى اسم عربي"""
    arabic_months = {
        1: 'يناير',
        2: 'فبراير',
        3: 'مارس',
        4: 'أبريل',
        5: 'مايو',
        6: 'يونيو',
        7: 'يوليو',
        8: 'أغسطس',
        9: 'سبتمبر',
        10: 'أكتوبر',
        11: 'نوفمبر',
        12: 'ديسمبر',
    }
    return arabic_months.get(month_number, '')


@login_required
def dashboard_stats(request):
    """إحصائيات تفصيلية محسّنة"""
    user = request.user
    
    # Get date range
    today = timezone.now()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    last_90_days = today - timedelta(days=90)
    
    businesses = Business.objects.filter(owner=user)
    
    # Check if user has no data
    if businesses.count() == 0:
        messages.info(
            request,
            'لا توجد بيانات لهذا المستخدم. '
            'للاختبار ببيانات تجريبية، '
            'سجّل خروج ودخول بـ: ahmed_owner '
            '(كلمة المرور: test123)'
        )
    
    # Comprehensive Statistics
    stats = {
        'overview': {
            'total_businesses': businesses.count(),
            'active_businesses': businesses.filter(is_active=True).count(),
            'verified_businesses': businesses.filter(is_verified=True).count(),
            'featured_businesses': businesses.filter(is_featured=True).count(),
            'pending_verification': businesses.filter(
                is_verified=False,
                is_active=True
            ).count(),
        },
        
        'businesses': {
            'total': businesses.count(),
            'active': businesses.filter(is_active=True).count(),
            'verified': businesses.filter(is_verified=True).count(),
            'featured': businesses.filter(is_featured=True).count(),
            'by_type': list(businesses.values('business_type').annotate(
                count=Count('id')
            )),
            'new_last_30_days': businesses.filter(
                created_at__gte=last_30_days
            ).count(),
        },
        
        'products': {
            'total': Product.objects.filter(business__owner=user).count(),
            'available': Product.objects.filter(
                business__owner=user, 
                is_available=True
            ).count(),
            'products': Product.objects.filter(
                business__owner=user,
                product_type='product'
            ).count(),
            'services': Product.objects.filter(
                business__owner=user,
                product_type='service'
            ).count(),
            'featured': Product.objects.filter(
                business__owner=user,
                is_featured=True
            ).count(),
            'new_last_30_days': Product.objects.filter(
                business__owner=user,
                created_at__gte=last_30_days
            ).count(),
        },
        
        'deals': {
            'total': Deal.objects.filter(business__owner=user).count(),
            'active': Deal.objects.filter(
                business__owner=user,
                start_date__lte=today,
                end_date__gte=today
            ).count(),
            'upcoming': Deal.objects.filter(
                business__owner=user,
                start_date__gt=today
            ).count(),
            'expired': Deal.objects.filter(
                business__owner=user,
                end_date__lt=today
            ).count(),
            'by_type': list(Deal.objects.filter(
                business__owner=user
            ).values('deal_type').annotate(count=Count('id'))),
            'featured': Deal.objects.filter(
                business__owner=user,
                is_featured=True
            ).count(),
        },
        
        'engagement': {
            'total_views': businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0,
            'total_clicks': businesses.aggregate(Sum('click_count'))['click_count__sum'] or 0,
            'views_last_7': calculate_period_views(businesses, last_7_days, today),
            'views_last_30': calculate_period_views(businesses, last_30_days, today),
            'clicks_last_7': calculate_period_clicks(businesses, last_7_days, today),
            'clicks_last_30': calculate_period_clicks(businesses, last_30_days, today),
        },
        
        'reviews': {
            'total': Review.objects.filter(business__owner=user).count(),
            'approved': Review.objects.filter(
                business__owner=user,
                is_approved=True
            ).count(),
            'pending': Review.objects.filter(
                business__owner=user,
                is_approved=False
            ).count(),
            'average_rating': Review.objects.filter(
                business__owner=user,
                is_approved=True
            ).aggregate(Avg('rating'))['rating__avg'] or 0,
            'last_30_days': Review.objects.filter(
                business__owner=user,
                created_at__gte=last_30_days
            ).count(),
        },
    }
    
    # Top performing businesses
    top_businesses = businesses.order_by('-view_count')[:10]
    
    # Recent activity
    recent_reviews = Review.objects.filter(
        business__owner=user
    ).select_related('business', 'user').order_by('-created_at')[:10]
    
    context = {
        'stats': stats,
        'top_businesses': top_businesses,
        'recent_reviews': recent_reviews,
        'has_data': businesses.count() > 0,
    }
    
    return render(request, 'dashboard/stats.html', context)


def calculate_period_views(businesses, start_date, end_date):
    """حساب المشاهدات في فترة محددة"""
    # This is a simplified version - you might want to track views with timestamps
    return businesses.filter(
        created_at__range=[start_date, end_date]
    ).aggregate(Sum('view_count'))['view_count__sum'] or 0


def calculate_period_clicks(businesses, start_date, end_date):
    """حساب النقرات في فترة محددة"""
    # This is a simplified version - you might want to track clicks with timestamps
    return businesses.filter(
        created_at__range=[start_date, end_date]
    ).aggregate(Sum('click_count'))['click_count__sum'] or 0
