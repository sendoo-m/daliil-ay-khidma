"""
Main Dashboard Views
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from apps.directory.models import Business
from apps.products.models import Product
from apps.deals.models import Deal


@login_required
def dashboard_home(request):
    """الصفحة الرئيسية للداش بورد"""
    user = request.user
    
    # Get user's businesses
    businesses = Business.objects.filter(owner=user)
    
    # Statistics
    stats = {
        'total_businesses': businesses.count(),
        'active_businesses': businesses.filter(is_active=True).count(),
        'verified_businesses': businesses.filter(is_verified=True).count(),
        'total_products': Product.objects.filter(business__owner=user).count(),
        'active_products': Product.objects.filter(
            business__owner=user, 
            is_available=True
        ).count(),
        'total_deals': Deal.objects.filter(business__owner=user).count(),
        'active_deals': Deal.objects.filter(
            business__owner=user,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).count(),
        'total_views': businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0,
        'total_clicks': businesses.aggregate(Sum('click_count'))['click_count__sum'] or 0,
    }
    
    # Recent businesses
    recent_businesses = businesses.order_by('-created_at')[:5]
    
    # Recent products
    recent_products = Product.objects.filter(
        business__owner=user
    ).select_related('business').order_by('-created_at')[:5]
    
    # Active deals
    active_deals = Deal.objects.filter(
        business__owner=user,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).select_related('business').order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_businesses': recent_businesses,
        'recent_products': recent_products,
        'active_deals': active_deals,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_stats(request):
    """إحصائيات تفصيلية"""
    user = request.user
    
    # Get date range (last 30 days)
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    
    businesses = Business.objects.filter(owner=user)
    
    # Detailed statistics
    stats = {
        'businesses': {
            'total': businesses.count(),
            'active': businesses.filter(is_active=True).count(),
            'verified': businesses.filter(is_verified=True).count(),
            'featured': businesses.filter(is_featured=True).count(),
            'by_type': businesses.values('business_type').annotate(
                count=Count('id')
            ),
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
        },
        'deals': {
            'total': Deal.objects.filter(business__owner=user).count(),
            'active': Deal.objects.filter(
                business__owner=user,
                start_date__lte=today,
                end_date__gte=today
            ).count(),
            'by_type': Deal.objects.filter(
                business__owner=user
            ).values('deal_type').annotate(count=Count('id')),
        },
        'engagement': {
            'total_views': businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0,
            'total_clicks': businesses.aggregate(Sum('click_count'))['click_count__sum'] or 0,
            'views_last_30': businesses.filter(
                created_at__gte=last_30_days
            ).aggregate(Sum('view_count'))['view_count__sum'] or 0,
        }
    }
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'dashboard/stats.html', context)
