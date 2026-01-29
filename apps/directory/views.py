"""
Directory App Views
===================
جميع عرض وعمليات الدليل
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .models import (
    Governorate,
    City,
    District,
    Category,
    Business,
    Favorite
)


# ========================================
# Home Page
# ========================================
def home(request):
    """الصفحة الرئيسية"""
    context = {
        'featured_businesses': Business.objects.filter(
            is_active=True,
            is_verified=True,
            is_featured=True
        )[:6],
        'promoted_businesses': Business.objects.filter(
            is_active=True,
            is_verified=True,
            is_promoted=True
        )[:3],
        'governorates': Governorate.objects.filter(is_active=True)[:8],
        'categories': Category.objects.filter(
            is_active=True,
            parent__isnull=True
        )[:8],
        'recent_businesses': Business.objects.filter(
            is_active=True,
            is_verified=True
        )[:6],
    }
    return render(request, 'directory/home.html', context)


# ========================================
# Governorate Views
# ========================================
def governorate_list(request):
    """قائمة المحافظات"""
    governorates = Governorate.objects.filter(is_active=True)
    
    context = {
        'governorates': governorates,
        'total_count': governorates.count()
    }
    return render(request, 'directory/governorate_list.html', context)


def governorate_detail(request, slug):
    """تفاصيل محافظة"""
    governorate = get_object_or_404(Governorate, slug=slug, is_active=True)
    
    cities = governorate.cities.filter(is_active=True)
    businesses = Business.objects.filter(
        district__city__governorate=governorate,
        is_active=True,
        is_verified=True
    )
    
    context = {
        'governorate': governorate,
        'cities': cities,
        'businesses': businesses[:12],
        'total_businesses': businesses.count()
    }
    return render(request, 'directory/governorate_detail.html', context)


# ========================================
# City Views
# ========================================
def city_detail(request, slug):
    """تفاصيل مدينة"""
    city = get_object_or_404(City, slug=slug, is_active=True)
    
    districts = city.districts.filter(is_active=True)
    businesses = Business.objects.filter(
        district__city=city,
        is_active=True,
        is_verified=True
    )
    
    context = {
        'city': city,
        'districts': districts,
        'businesses': businesses[:12],
        'total_businesses': businesses.count()
    }
    return render(request, 'directory/city_detail.html', context)


# ========================================
# District Views
# ========================================
def district_detail(request, slug):
    """تفاصيل حي"""
    district = get_object_or_404(District, slug=slug, is_active=True)
    
    businesses = Business.objects.filter(
        district=district,
        is_active=True,
        is_verified=True
    )
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    context = {
        'district': district,
        'businesses': businesses_page,
        'total_businesses': businesses.count()
    }
    return render(request, 'directory/district_detail.html', context)


# ========================================
# Category Views
# ========================================
def category_list(request):
    """قائمة الفئات"""
    categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    )
    
    context = {
        'categories': categories,
        'total_count': categories.count()
    }
    return render(request, 'directory/category_list.html', context)


def category_detail(request, slug):
    """تفاصيل فئة"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Get all subcategories
    subcategories = category.children.filter(is_active=True)
    
    # Get businesses in this category and subcategories
    categories_ids = [category.id] + list(
        subcategories.values_list('id', flat=True)
    )
    
    businesses = Business.objects.filter(
        category_id__in=categories_ids,
        is_active=True,
        is_verified=True
    )
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'businesses': businesses_page,
        'total_businesses': businesses.count()
    }
    return render(request, 'directory/category_detail.html', context)


# ========================================
# Business Views
# ========================================
def business_list(request):
    """قائمة جميع المحلات"""
    businesses = Business.objects.filter(
        is_active=True,
        is_verified=True
    )
    
    # Filters
    category_slug = request.GET.get('category')
    governorate_slug = request.GET.get('governorate')
    city_slug = request.GET.get('city')
    search = request.GET.get('q')
    
    if category_slug:
        businesses = businesses.filter(category__slug=category_slug)
    
    if governorate_slug:
        businesses = businesses.filter(
            district__city__governorate__slug=governorate_slug
        )
    
    if city_slug:
        businesses = businesses.filter(district__city__slug=city_slug)
    
    if search:
        businesses = businesses.filter(
            Q(name_en__icontains=search) |
            Q(name_ar__icontains=search) |
            Q(description_en__icontains=search) |
            Q(description_ar__icontains=search)
        )
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if sort == 'popular':
        businesses = businesses.order_by('-view_count')
    elif sort == 'rating':
        # This will be implemented when reviews are added
        businesses = businesses.order_by('-created_at')
    else:
        businesses = businesses.order_by(sort)
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    context = {
        'businesses': businesses_page,
        'total_count': businesses.count(),
        'categories': Category.objects.filter(is_active=True, parent__isnull=True),
        'governorates': Governorate.objects.filter(is_active=True),
    }
    return render(request, 'directory/business_list.html', context)


def business_detail(request, slug):
    """تفاصيل محل تجاري"""
    business = get_object_or_404(
        Business,
        slug=slug,
        is_active=True
    )
    
    # Increment view count
    business.increment_view_count()
    
    # Check if user has favorited this business
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=request.user,
            business=business
        ).exists()
    
    # Get related businesses
    related_businesses = Business.objects.filter(
        category=business.category,
        is_active=True,
        is_verified=True
    ).exclude(id=business.id)[:4]
    
    context = {
        'business': business,
        'is_favorited': is_favorited,
        'related_businesses': related_businesses,
        'images': business.images.filter(is_active=True)
    }
    return render(request, 'directory/business_detail.html', context)


# ========================================
# Business CRUD (Owner)
# ========================================
@login_required
def business_create(request):
    """إضافة محل جديد"""
    # This will be implemented with forms
    return render(request, 'directory/business_form.html')


@login_required
def business_update(request, slug):
    """تعديل محل"""
    business = get_object_or_404(
        Business,
        slug=slug,
        owner=request.user
    )
    # This will be implemented with forms
    return render(request, 'directory/business_form.html', {'business': business})


@login_required
def business_delete(request, slug):
    """حذف محل"""
    business = get_object_or_404(
        Business,
        slug=slug,
        owner=request.user
    )
    if request.method == 'POST':
        business.delete()
        messages.success(request, 'Business deleted successfully!')
        return redirect('directory:my_businesses')
    
    return render(request, 'directory/business_confirm_delete.html', {'business': business})


# ========================================
# User Dashboard
# ========================================
@login_required
def my_businesses(request):
    """محلاتي"""
    businesses = Business.objects.filter(owner=request.user)
    
    context = {
        'businesses': businesses,
        'total_count': businesses.count()
    }
    return render(request, 'directory/my_businesses.html', context)


@login_required
def my_favorites(request):
    """مفضلاتي"""
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('business')
    
    context = {
        'favorites': favorites,
        'total_count': favorites.count()
    }
    return render(request, 'directory/my_favorites.html', context)


# ========================================
# Favorite Toggle
# ========================================
@login_required
@require_POST
def favorite_toggle(request, slug):
    """إضافة/إزالة من المفضلة"""
    business = get_object_or_404(Business, slug=slug)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        business=business
    )
    
    if not created:
        favorite.delete()
        message = 'Removed from favorites'
        is_favorited = False
    else:
        message = 'Added to favorites'
        is_favorited = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'is_favorited': is_favorited
        })
    
    messages.success(request, message)
    return redirect('directory:business_detail', slug=slug)


# ========================================
# AJAX Endpoints
# ========================================
@require_POST
def increment_view(request, slug):
    """زيادة عداد المشاهدات"""
    business = get_object_or_404(Business, slug=slug)
    business.increment_view_count()
    
    return JsonResponse({
        'success': True,
        'view_count': business.view_count
    })


@require_POST
def increment_click(request, slug):
    """زيادة عداد النقرات"""
    business = get_object_or_404(Business, slug=slug)
    business.increment_click_count()
    
    return JsonResponse({
        'success': True,
        'click_count': business.click_count
    })
