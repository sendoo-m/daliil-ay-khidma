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

from apps.directory.models.favorites import Favorite

from .models import (
    Governorate,
    City,
    District,
    Category,
    Business
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


# def business_detail(request, slug):
#     """تفاصيل محل تجاري"""
#     business = get_object_or_404(
#         Business,
#         slug=slug,
#         is_active=True
#     )
    
#     # Increment view count
#     business.increment_view_count()
    
#     # Check if user has favorited this business
#     is_favorited = False
#     if request.user.is_authenticated:
#         is_favorited = Favorite.objects.filter(
#             user=request.user,
#             business=business
#         ).exists()
    
#     # Get related businesses
#     related_businesses = Business.objects.filter(
#         category=business.category,
#         is_active=True,
#         is_verified=True
#     ).exclude(id=business.id)[:4]
    
#     context = {
#         'business': business,
#         'is_favorited': is_favorited,
#         'related_businesses': related_businesses,
#         'images': business.images.filter(is_active=True)
#     }
#     return render(request, 'directory/business_detail.html', context)
def business_detail(request, slug):
    """تفاصيل محل معين"""
    business = get_object_or_404(
        Business.objects.select_related(
            'category',
            'district__city__governorate',
            'owner'
        ),
        slug=slug
    )
    
    # Increment view count
    business.increment_view_count()
    
    # Get business images
    images = business.images.filter(is_active=True)
    
    # Get products من تطبيق products
    from apps.products.models import Product
    products = Product.objects.filter(
        business=business,
        is_available=True
    ).prefetch_related('images').order_by('-is_featured', 'order', '-created_at')
    
    # Get reviews (if reviews app exists)
    reviews = None
    average_rating = 0
    total_reviews = 0
    try:
        from apps.reviews.models import Review
        from django.db.models import Avg
        
        reviews = Review.objects.filter(
            business=business,
            is_approved=True
        ).select_related('user').order_by('-created_at')[:5]
        
        if reviews.exists():
            avg = Review.objects.filter(
                business=business,
                is_approved=True
            ).aggregate(Avg('rating'))['rating__avg']
            average_rating = round(avg, 1) if avg else 0
            total_reviews = Review.objects.filter(
                business=business,
                is_approved=True
            ).count()
    except ImportError:
        pass
    
    # Check if user favorited
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=request.user,
            business=business
        ).exists()
    
    # Related businesses (same category)
    related_businesses = Business.objects.filter(
        category=business.category,
        is_active=True,
        is_verified=True
    ).exclude(id=business.id).order_by('-is_featured', '-view_count')[:5]
    
    context = {
        'business': business,
        'images': images,
        'products': products,
        'reviews': reviews,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'is_favorited': is_favorited,
        'related_businesses': related_businesses,
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


# ========================================
# Search View
# ========================================
def business_search(request):
    """البحث في المحلات"""
    query = request.GET.get('q', '').strip()
    businesses = Business.objects.filter(
        is_active=True,
        is_verified=True
    ).select_related('category', 'district__city__governorate')
    
    if query:
        businesses = businesses.filter(
            Q(name_en__icontains=query) |
            Q(name_ar__icontains=query) |
            Q(description_en__icontains=query) |
            Q(description_ar__icontains=query) |
            Q(category__name_en__icontains=query) |
            Q(category__name_ar__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(businesses, 12)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    context = {
        'businesses': businesses_page,
        'query': query,
        'total_results': businesses.count(),
        'page_title': f'Search: {query}' if query else 'Search',
    }
    
    return render(request, 'directory/business_search.html', context)


from django.shortcuts import render
from django.db.models import Q
from apps.directory.models import Business, Governorate
from apps.categories.models import Category
import json


def map_view(request):
    """خريطة المحلات التفاعلية"""
    
    # Get all active businesses with coordinates
    businesses = Business.objects.filter(
        is_active=True,
        is_verified=True,
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related(
        'category',
        'district__city__governorate'
    )
    
    # Convert to list of dicts for JSON
    businesses_data = []
    for business in businesses:
        businesses_data.append({
            'id': business.id,
            'name_en': business.name_en,
            'name_ar': business.name_ar,
            'slug': business.slug,
            'latitude': float(business.latitude),
            'longitude': float(business.longitude),
            'logo': business.logo.url if business.logo else '',
            'business_type': business.business_type,
            'category_name_en': business.category.name_en,
            'category_name_ar': business.category.name_ar,
            'category_icon': business.category.icon,
            'district_name_en': business.district.name_en,
            'city_name_en': business.district.city.name_en,
            'governorate_name_en': business.district.city.governorate.name_en,
            'phone': business.phone,
            'is_featured': business.is_featured,
        })
    
    # Get filters
    categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    ).order_by('order')
    
    governorates = Governorate.objects.filter(
        is_active=True
    ).order_by('order')
    
    context = {
        'businesses_json': json.dumps(businesses_data),
        'categories': categories,
        'governorates': governorates,
        'total_businesses': len(businesses_data),
    }
    
    return render(request, 'directory/map.html', context)
