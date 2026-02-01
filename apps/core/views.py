"""
Core Views
==========
Views للصفحات الأساسية
"""

from django.shortcuts import render, redirect
from django.utils.translation import activate, get_language
from django.conf import settings
from django.db.models import Count, Q
from apps.directory.models import Business, Category, Governorate
from apps.deals.models import Deal


def home(request):
    """الصفحة الرئيسية"""
    
    # Featured Categories
    featured_categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    ).annotate(
        business_count=Count('business', filter=Q(business__is_active=True))
    ).order_by('order')[:8]
    
    # Latest Businesses
    latest_businesses = Business.objects.filter(
        is_active=True,
        is_verified=True
    ).select_related('category', 'district__city__governorate').order_by('-created_at')[:8]
    
    # Featured Businesses
    featured_businesses = Business.objects.filter(
        is_active=True,
        is_featured=True,
        is_verified=True
    ).select_related('category', 'district__city__governorate')[:6]
    
    # Most Viewed
    most_viewed_businesses = Business.objects.filter(
        is_active=True,
        is_verified=True
    ).select_related('category', 'district__city__governorate').order_by('-view_count')[:6]
    
    # Governorates
    governorates = Governorate.objects.filter(
        is_active=True
    ).order_by('order')[:6]
    
    # Active Deals
    active_deals = Deal.objects.filter(
        is_active=True,
        business__is_active=True
    ).select_related('business').order_by('-created_at')[:6]
    
    # Statistics
    stats = {
        'total_businesses': Business.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_deals': Deal.objects.filter(is_active=True).count(),
        'verified_businesses': Business.objects.filter(is_active=True, is_verified=True).count(),
    }
    
    context = {
        'featured_categories': featured_categories,
        'latest_businesses': latest_businesses,
        'featured_businesses': featured_businesses,
        'most_viewed_businesses': most_viewed_businesses,
        'governorates': governorates,
        'active_deals': active_deals,
        'stats': stats,
    }
    
    return render(request, 'core/home.html', context)


def set_language(request):
    """تبديل اللغة"""
    language = request.GET.get('language', 'ar')
    
    # Validate language
    if language in [lang[0] for lang in settings.LANGUAGES]:
        activate(language)
        request.session[settings.LANGUAGE_COOKIE_NAME] = language
    
    # Get redirect URL
    next_url = request.GET.get('next')
    if not next_url:
        next_url = request.META.get('HTTP_REFERER', '/')
    
    response = redirect(next_url)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language,
        max_age=365 * 24 * 60 * 60  # 1 year
    )
    
    return response


def about(request):
    """صفحة عن الموقع"""
    return render(request, 'core/about.html')


def contact(request):
    """صفحة اتصل بنا"""
    return render(request, 'core/contact.html')

# # apps/core/views.py
# from django.shortcuts import render, redirect
# from django.db.models import Count, Q
# from django.conf import settings
# from apps.directory.models import Business, Category, Governorate
# from apps.deals.models import Deal


# def home(request):
#     """الصفحة الرئيسية المحسّنة"""
    
#     # Featured Businesses (المميزة)
#     featured_businesses = Business.objects.filter(
#         is_active=True,
#         is_featured=True,
#         is_verified=True
#     ).select_related('category', 'district__city__governorate')[:6]
    
#     # Latest Businesses (الأحدث)
#     latest_businesses = Business.objects.filter(
#         is_active=True,
#         is_verified=True
#     ).select_related('category', 'district__city__governorate').order_by('-created_at')[:8]
    
#     # Most Viewed (الأكثر مشاهدة)
#     most_viewed_businesses = Business.objects.filter(
#         is_active=True,
#         is_verified=True
#     ).select_related('category', 'district__city__governorate').order_by('-view_count')[:6]
    
#     # Categories (التصنيفات)
#     categories = Category.objects.filter(
#         is_active=True,
#         parent__isnull=True
#     ).annotate(
#         business_count=Count('business', filter=Q(business__is_active=True))
#     ).order_by('order')[:8]
    
#     # Governorates (المحافظات)
#     governorates = Governorate.objects.filter(
#         is_active=True
#     ).order_by('name_ar')[:6]
    
#     # Active Deals (العروض النشطة)
#     active_deals = Deal.objects.filter(
#         is_active=True,
#         business__is_active=True
#     ).select_related('business')[:8]
    
#     # Stats (الإحصائيات)
#     stats = {
#         'total_businesses': Business.objects.filter(is_active=True).count(),
#         'total_categories': Category.objects.filter(is_active=True).count(),
#         'total_deals': Deal.objects.filter(is_active=True).count(),
#         'total_governorates': Governorate.objects.filter(is_active=True).count(),
#     }
    
#     context = {
#         'featured_businesses': featured_businesses,
#         'latest_businesses': latest_businesses,
#         'most_viewed_businesses': most_viewed_businesses,
#         'categories': categories,
#         'governorates': governorates,
#         'active_deals': active_deals,
#         'stats': stats,
#     }
    
#     return render(request, 'core/home.html', context)

# """
# Core Views
# ==========
# Views للصفحات الأساسية
# """

# from django.shortcuts import render, redirect
# from django.utils.translation import activate
# from django.conf import settings
# from apps.directory.models import Business, Category
# from apps.deals.models import Deal


# def home(request):
#     """الصفحة الرئيسية"""
    
#     # Featured Categories
#     featured_categories = Category.objects.filter(
#         is_active=True,
#         parent__isnull=True
#     ).order_by('order')[:8]
    
#     # Latest Businesses
#     latest_businesses = Business.objects.filter(
#         is_active=True,
#         is_verified=True
#     ).select_related('category', 'district__city__governorate').order_by('-created_at')[:8]
    
#     # Featured Businesses
#     featured_businesses = Business.objects.filter(
#         is_active=True,
#         is_featured=True
#     ).select_related('category', 'district__city__governorate').order_by('?')[:6]
    
#     # Active Deals
#     active_deals = Deal.objects.filter(
#         is_active=True
#     ).select_related('business').order_by('-created_at')[:6]
    
#     # Statistics
#     stats = {
#         'total_businesses': Business.objects.filter(is_active=True).count(),
#         'total_categories': Category.objects.filter(is_active=True).count(),
#         'total_deals': Deal.objects.filter(is_active=True).count(),
#         'verified_businesses': Business.objects.filter(is_active=True, is_verified=True).count(),
#     }
    
#     context = {
#         'featured_categories': featured_categories,
#         'latest_businesses': latest_businesses,
#         'featured_businesses': featured_businesses,
#         'active_deals': active_deals,
#         'stats': stats,
#     }
    
#     return render(request, 'core/home.html', context)


# def set_language(request):
#     """تبديل اللغة"""
#     language = request.GET.get('language', 'ar')
    
#     if language in [lang[0] for lang in settings.LANGUAGES]:
#         activate(language)
#         request.session['django_language'] = language
    
#     # Redirect to previous page or home
#     next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
#     return redirect(next_url)


# def about(request):
#     return render(request, 'core/about.html')


# def contact(request):
#     return render(request, 'core/contact.html')


def test_icons(request):
    return render(request, 'test_icons.html')
