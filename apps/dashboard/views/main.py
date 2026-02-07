"""
Main Dashboard Views
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

from apps.directory.models import Business
from apps.products.models import Product
from apps.deals.models import Deal
from apps.reviews.models import Review


@login_required
def dashboard_home(request):
    """الصفحة الرئيسية المحسّنة للداش بورد"""
    user = request.user
    
    # Get user's businesses with related data
    businesses = Business.objects.filter(owner=user).select_related('category')
    
    # Today and date calculations
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    
    # Core Statistics
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
        
        'total_deals': Deal.objects.filter(business__owner=user).count(),
        'active_deals': Deal.objects.filter(
            business__owner=user,
            start_date__lte=today,
            end_date__gte=today
        ).count(),
        
        'total_views': businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0,
        'total_clicks': businesses.aggregate(Sum('click_count'))['click_count__sum'] or 0,
    }
    
    # Business Type Breakdown
    business_types = businesses.values('business_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Reviews Statistics
    total_reviews = Review.objects.filter(business__owner=user).count()
    approved_reviews = Review.objects.filter(
        business__owner=user,
        is_approved=True
    ).count()
    
    avg_rating = Review.objects.filter(
        business__owner=user,
        is_approved=True
    ).aggregate(Avg('rating'))['rating__avg'] or 0
    
    stats['total_reviews'] = total_reviews
    stats['approved_reviews'] = approved_reviews
    stats['avg_rating'] = round(avg_rating, 1)
    
    # Recent Activities
    recent_businesses = businesses.select_related('category').order_by('-created_at')[:5]
    
    recent_products = Product.objects.filter(
        business__owner=user
    ).select_related('business').order_by('-created_at')[:5]
    
    active_deals = Deal.objects.filter(
        business__owner=user,
        start_date__lte=today,
        end_date__gte=today
    ).select_related('business').order_by('-created_at')[:5]
    
    recent_reviews = Review.objects.filter(
        business__owner=user
    ).select_related('business', 'user').order_by('-created_at')[:5]
    
    # Monthly Performance (last 6 months)
    monthly_data = []
    for i in range(5, -1, -1):
        month_start = today - timedelta(days=30*i)
        month_end = today - timedelta(days=30*(i-1)) if i > 0 else today
        
        month_views = businesses.filter(
            created_at__lte=month_end
        ).aggregate(Sum('view_count'))['view_count__sum'] or 0
        
        monthly_data.append({
            'month': month_start.strftime('%B'),
            'views': month_views,
        })
    
    # Growth Indicators
    last_week_businesses = businesses.filter(created_at__gte=last_7_days).count()
    last_week_products = Product.objects.filter(
        business__owner=user,
        created_at__gte=last_7_days
    ).count()
    
    stats['new_businesses_week'] = last_week_businesses
    stats['new_products_week'] = last_week_products
    
    context = {
        'stats': stats,
        'business_types': business_types,
        'recent_businesses': recent_businesses,
        'recent_products': recent_products,
        'active_deals': active_deals,
        'recent_reviews': recent_reviews,
        'monthly_data': monthly_data,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_stats(request):
    """إحصائيات تفصيلية متقدمة"""
    user = request.user
    
    # Get date range (last 30 days)
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    
    businesses = Business.objects.filter(owner=user)
    
    # Detailed Business Statistics
    business_stats = {
        'total': businesses.count(),
        'active': businesses.filter(is_active=True).count(),
        'verified': businesses.filter(is_verified=True).count(),
        'featured': businesses.filter(is_featured=True).count(),
        'pending': businesses.filter(is_verified=False).count(),
        'by_type': businesses.values('business_type').annotate(
            count=Count('id')
        ),
        'new_this_week': businesses.filter(created_at__gte=last_7_days).count(),
        'new_this_month': businesses.filter(created_at__gte=last_30_days).count(),
    }
    
    # Detailed Product Statistics
    product_stats = {
        'total': Product.objects.filter(business__owner=user).count(),
        'available': Product.objects.filter(
            business__owner=user, 
            is_available=True
        ).count(),
        'unavailable': Product.objects.filter(
            business__owner=user, 
            is_available=False
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
        'new_this_week': Product.objects.filter(
            business__owner=user,
            created_at__gte=last_7_days
        ).count(),
    }
    
    # Detailed Deal Statistics
    deal_stats = {
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
        'by_type': Deal.objects.filter(
            business__owner=user
        ).values('deal_type').annotate(count=Count('id')),
        'featured': Deal.objects.filter(
            business__owner=user,
            is_featured=True
        ).count(),
    }
    
    # Engagement & Performance
    engagement_stats = {
        'total_views': businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0,
        'total_clicks': businesses.aggregate(Sum('click_count'))['click_count__sum'] or 0,
        'views_last_30': businesses.filter(
            updated_at__gte=last_30_days
        ).aggregate(Sum('view_count'))['view_count__sum'] or 0,
        'clicks_last_30': businesses.filter(
            updated_at__gte=last_30_days
        ).aggregate(Sum('click_count'))['click_count__sum'] or 0,
    }
    
    # Calculate Click-Through Rate (CTR)
    if engagement_stats['total_views'] > 0:
        engagement_stats['ctr'] = round(
            (engagement_stats['total_clicks'] / engagement_stats['total_views']) * 100, 
            2
        )
    else:
        engagement_stats['ctr'] = 0
    
    # Review Statistics
    review_stats = {
        'total': Review.objects.filter(business__owner=user).count(),
        'approved': Review.objects.filter(
            business__owner=user,
            is_approved=True
        ).count(),
        'pending': Review.objects.filter(
            business__owner=user,
            is_approved=False
        ).count(),
        'with_reply': Review.objects.filter(
            business__owner=user,
            reply__isnull=False
        ).count(),
        'avg_rating': Review.objects.filter(
            business__owner=user,
            is_approved=True
        ).aggregate(Avg('rating'))['rating__avg'] or 0,
    }
    
    review_stats['avg_rating'] = round(review_stats['avg_rating'], 1)
    
    # Top Performing Businesses
    top_businesses = businesses.order_by('-view_count')[:5]
    
    # Recent Activity
    recent_activity = []
    
    # Recent businesses
    for business in businesses.order_by('-created_at')[:3]:
        recent_activity.append({
            'type': 'business',
            'title': business.name_ar,
            'date': business.created_at,
            'icon': 'fa-store',
            'color': 'primary'
        })
    
    # Recent products
    for product in Product.objects.filter(business__owner=user).order_by('-created_at')[:3]:
        recent_activity.append({
            'type': 'product',
            'title': product.name_ar,
            'date': product.created_at,
            'icon': 'fa-box',
            'color': 'success'
        })
    
    # Sort by date
    recent_activity = sorted(recent_activity, key=lambda x: x['date'], reverse=True)[:10]
    
    context = {
        'business_stats': business_stats,
        'product_stats': product_stats,
        'deal_stats': deal_stats,
        'engagement_stats': engagement_stats,
        'review_stats': review_stats,
        'top_businesses': top_businesses,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'dashboard/stats.html', context)
