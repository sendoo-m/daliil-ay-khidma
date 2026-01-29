# apps/core/views.py
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.utils import translation
from django.conf import settings
from apps.directory.models import Business, Category, Governorate
from apps.deals.models import Deal


def home(request):
    """الصفحة الرئيسية المحسّنة"""
    
    # Featured Businesses (المميزة)
    featured_businesses = Business.objects.filter(
        is_active=True,
        is_featured=True,
        is_verified=True
    ).select_related('category', 'district__city__governorate')[:6]
    
    # Latest Businesses (الأحدث)
    latest_businesses = Business.objects.filter(
        is_active=True,
        is_verified=True
    ).select_related('category', 'district__city__governorate').order_by('-created_at')[:8]
    
    # Most Viewed (الأكثر مشاهدة)
    most_viewed_businesses = Business.objects.filter(
        is_active=True,
        is_verified=True
    ).select_related('category', 'district__city__governorate').order_by('-view_count')[:6]
    
    # Categories (التصنيفات)
    categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    ).annotate(
        business_count=Count('business', filter=Q(business__is_active=True))
    ).order_by('order')[:8]
    
    # Governorates (المحافظات)
    governorates = Governorate.objects.filter(
        is_active=True
    ).order_by('name_ar')[:6]
    
    # Active Deals (العروض النشطة)
    active_deals = Deal.objects.filter(
        is_active=True,
        business__is_active=True
    ).select_related('business')[:8]
    
    # Stats (الإحصائيات)
    stats = {
        'total_businesses': Business.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_deals': Deal.objects.filter(is_active=True).count(),
        'total_governorates': Governorate.objects.filter(is_active=True).count(),
    }
    
    context = {
        'featured_businesses': featured_businesses,
        'latest_businesses': latest_businesses,
        'most_viewed_businesses': most_viewed_businesses,
        'categories': categories,
        'governorates': governorates,
        'active_deals': active_deals,
        'stats': stats,
    }
    
    return render(request, 'core/home.html', context)


def change_language(request):
    """تغيير اللغة"""
    lang_code = request.GET.get('lang', 'ar')
    
    # التأكد من أن اللغة مدعومة
    if lang_code not in [lang[0] for lang in settings.LANGUAGES]:
        lang_code = 'ar'
    
    # تفعيل اللغة الجديدة
    translation.activate(lang_code)
    
    # حفظ اللغة في الـ session
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    
    # الرجوع للصفحة السابقة
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    
    response = redirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    
    return response


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def test_icons(request):
    return render(request, 'test_icons.html')
