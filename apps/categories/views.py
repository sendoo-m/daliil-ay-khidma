"""
Categories Views
===============
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Category


def category_list(request):
    """قائمة التصنيفات"""
    
    categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    ).annotate(
        business_count=Count(
            'business_set',
            filter=Q(business_set__is_active=True)
        )
    ).order_by('order', 'name_en')
    
    context = {
        'categories': categories,
        'total_count': categories.count(),
    }
    
    return render(request, 'categories/category_list.html', context)


def category_detail(request, slug):
    """تفاصيل التصنيف"""
    
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Get businesses
    businesses = category.business_set.filter(
        is_active=True
    ).select_related(
        'category', 'district__city__governorate'
    ).order_by('-is_featured', '-created_at')[:12]
    
    # Sub-categories
    sub_categories = category.children.filter(
        is_active=True
    ).annotate(
        business_count=Count(
            'business_set',
            filter=Q(business_set__is_active=True)
        )
    ).order_by('order')
    
    context = {
        'category': category,
        'businesses': businesses,
        'sub_categories': sub_categories,
        'breadcrumb': category.get_breadcrumb(),
    }
    
    return render(request, 'categories/category_detail.html', context)




# # ========================================
# # Category Views
# # ========================================
# def category_list(request):
#     """قائمة الفئات"""
#     categories = Category.objects.filter(
#         is_active=True,
#         parent__isnull=True
#     )
    
#     context = {
#         'categories': categories,
#         'total_count': categories.count()
#     }
#     return render(request, 'directory/category_list.html', context)


# def category_detail(request, slug):
#     """تفاصيل فئة"""
#     category = get_object_or_404(Category, slug=slug, is_active=True)
    
#     # Get all subcategories
#     subcategories = category.children.filter(is_active=True)
    
#     # Get businesses in this category and subcategories
#     categories_ids = [category.id] + list(
#         subcategories.values_list('id', flat=True)
#     )
    
#     businesses = Business.objects.filter(
#         category_id__in=categories_ids,
#         is_active=True,
#         is_verified=True
#     )
    
#     # Pagination
#     paginator = Paginator(businesses, 20)
#     page = request.GET.get('page')
#     businesses_page = paginator.get_page(page)
    
#     context = {
#         'category': category,
#         'subcategories': subcategories,
#         'businesses': businesses_page,
#         'total_businesses': businesses.count()
#     }
#     return render(request, 'directory/category_detail.html', context)

