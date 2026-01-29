"""
Owner Dashboard Views
====================
Dashboard for business owners to manage their businesses, products, and deals
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.directory.models import Business, Category, District
from apps.products.models import Product, ProductImage
from apps.deals.models import Deal
from apps.reviews.models import Review
from apps.dashboard.decorators import business_owner_required


# ========================================
# Dashboard Home
# ========================================
@login_required
def owner_dashboard(request):
    """لوحة التحكم الرئيسية لصاحب المحل"""
    businesses = request.user.businesses.all()
    
    # إحصائيات عامة
    total_businesses = businesses.count()
    total_products = Product.objects.filter(business__owner=request.user).count()
    total_deals = Deal.objects.filter(business__owner=request.user).count()
    total_reviews = Review.objects.filter(business__owner=request.user).count()
    
    # متوسط التقييم
    avg_rating = Review.objects.filter(
        business__owner=request.user,
        is_approved=True
    ).aggregate(Avg('rating'))['rating__avg'] or 0
    
    # إجمالي المشاهدات
    total_views = sum(b.view_count for b in businesses)
    
    # آخر التعليقات
    recent_reviews = Review.objects.filter(
        business__owner=request.user
    ).select_related('business', 'user').order_by('-created_at')[:5]
    
    # التعليقات المنتظرة (بدون رد)
    pending_reviews = Review.objects.filter(
        business__owner=request.user,
        reply__isnull=True,
        is_approved=True
    ).count()
    
    context = {
        'businesses': businesses,
        'total_businesses': total_businesses,
        'total_products': total_products,
        'total_deals': total_deals,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
        'total_views': total_views,
        'recent_reviews': recent_reviews,
        'pending_reviews': pending_reviews,
    }
    
    return render(request, 'dashboard/owner/dashboard.html', context)


# ========================================
# Business Management
# ========================================
@login_required
def business_list(request):
    """قائمة محلات صاحب المحل"""
    businesses = request.user.businesses.all().select_related(
        'category', 'district__city'
    ).prefetch_related('images')
    
    # فلتر حسب النوع
    business_type = request.GET.get('type')
    if business_type:
        businesses = businesses.filter(business_type=business_type)
    
    context = {
        'businesses': businesses,
        'business_type': business_type,
    }
    
    return render(request, 'dashboard/owner/business_list.html', context)


@login_required
def business_create(request):
    """إضافة محل جديد"""
    if request.method == 'POST':
        # TODO: Use ModelForm
        business = Business(
            owner=request.user,
            business_type=request.POST.get('business_type', 'shop'),
            name_en=request.POST.get('name_en'),
            name_ar=request.POST.get('name_ar'),
            category_id=request.POST.get('category'),
            district_id=request.POST.get('district'),
            phone=request.POST.get('phone'),
            whatsapp=request.POST.get('whatsapp', ''),
            email=request.POST.get('email', ''),
            address_en=request.POST.get('address_en'),
            address_ar=request.POST.get('address_ar'),
            description_en=request.POST.get('description_en'),
            description_ar=request.POST.get('description_ar'),
        )
        
        if 'logo' in request.FILES:
            business.logo = request.FILES['logo']
        
        business.save()
        
        messages.success(request, 'تم إضافة المحل بنجاح! يرجى انتظار موافقة الإدارة.')
        return redirect('dashboard:business_detail', slug=business.slug)
    
    # GET request
    categories = Category.objects.filter(is_active=True)
    districts = District.objects.filter(is_active=True).select_related('city')
    
    context = {
        'categories': categories,
        'districts': districts,
    }
    
    return render(request, 'dashboard/owner/business_form.html', context)


@login_required
def business_detail(request, slug):
    """تفاصيل المحل"""
    business = get_object_or_404(
        Business,
        slug=slug,
        owner=request.user
    )
    
    # إحصائيات المحل
    products_count = business.products.count()
    deals_count = business.deals.count()
    reviews_count = business.total_reviews
    avg_rating = business.average_rating
    
    # آخر المنتجات
    recent_products = business.products.all()[:5]
    
    # آخر العروض
    recent_deals = business.deals.filter(
        end_date__gte=timezone.now()
    ).order_by('-created_at')[:5]
    
    context = {
        'business': business,
        'products_count': products_count,
        'deals_count': deals_count,
        'reviews_count': reviews_count,
        'avg_rating': avg_rating,
        'recent_products': recent_products,
        'recent_deals': recent_deals,
    }
    
    return render(request, 'dashboard/owner/business_detail.html', context)


@login_required
def business_edit(request, slug):
    """تعديل المحل"""
    business = get_object_or_404(
        Business,
        slug=slug,
        owner=request.user
    )
    
    if request.method == 'POST':
        # Update business
        business.business_type = request.POST.get('business_type', business.business_type)
        business.name_en = request.POST.get('name_en')
        business.name_ar = request.POST.get('name_ar')
        business.category_id = request.POST.get('category')
        business.district_id = request.POST.get('district')
        business.phone = request.POST.get('phone')
        business.whatsapp = request.POST.get('whatsapp', '')
        business.email = request.POST.get('email', '')
        business.address_en = request.POST.get('address_en')
        business.address_ar = request.POST.get('address_ar')
        business.description_en = request.POST.get('description_en')
        business.description_ar = request.POST.get('description_ar')
        business.working_hours_en = request.POST.get('working_hours_en', '')
        business.working_hours_ar = request.POST.get('working_hours_ar', '')
        
        if 'logo' in request.FILES:
            business.logo = request.FILES['logo']
        
        if 'cover_image' in request.FILES:
            business.cover_image = request.FILES['cover_image']
        
        business.save()
        
        messages.success(request, 'تم تحديث بيانات المحل بنجاح')
        return redirect('dashboard:business_detail', slug=business.slug)
    
    # GET request
    categories = Category.objects.filter(is_active=True)
    districts = District.objects.filter(is_active=True).select_related('city')
    
    context = {
        'business': business,
        'categories': categories,
        'districts': districts,
        'is_edit': True,
    }
    
    return render(request, 'dashboard/owner/business_form.html', context)


@require_POST
@login_required
def business_delete(request, slug):
    """حذف المحل"""
    business = get_object_or_404(
        Business,
        slug=slug,
        owner=request.user
    )
    
    business.delete()
    messages.success(request, 'تم حذف المحل بنجاح')
    return redirect('dashboard:business_list')


# ========================================
# Product Management
# ========================================
@business_owner_required
def product_list(request):
    """قائمة المنتجات"""
    products = Product.objects.filter(
        business__owner=request.user
    ).select_related('business').prefetch_related('images')
    
    # فلتر حسب المحل
    business_id = request.GET.get('business')
    if business_id:
        products = products.filter(business_id=business_id)
    
    # قائمة المحلات للفلتر
    businesses = request.user.businesses.all()
    
    context = {
        'products': products,
        'businesses': businesses,
        'selected_business': business_id,
    }
    
    return render(request, 'dashboard/owner/product_list.html', context)


@business_owner_required
def product_create(request):
    """إضافة منتج جديد"""
    if request.method == 'POST':
        product = Product(
            business_id=request.POST.get('business'),
            product_type=request.POST.get('product_type', 'product'),
            name_en=request.POST.get('name_en'),
            name_ar=request.POST.get('name_ar'),
            description_en=request.POST.get('description_en', ''),
            description_ar=request.POST.get('description_ar', ''),
            price=request.POST.get('price', 0),
            old_price=request.POST.get('old_price') or None,
        )
        
        product.save()
        
        # رفع الصور
        if 'images' in request.FILES:
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(
                    product=product,
                    image=image
                )
        
        messages.success(request, 'تم إضافة المنتج بنجاح')
        return redirect('dashboard:product_list')
    
    # GET request
    businesses = request.user.businesses.filter(is_active=True)
    
    context = {
        'businesses': businesses,
    }
    
    return render(request, 'dashboard/owner/product_form.html', context)


@business_owner_required
def product_edit(request, slug):
    """تعديل منتج"""
    product = get_object_or_404(
        Product,
        slug=slug,
        business__owner=request.user
    )
    
    if request.method == 'POST':
        product.product_type = request.POST.get('product_type', product.product_type)
        product.name_en = request.POST.get('name_en')
        product.name_ar = request.POST.get('name_ar')
        product.description_en = request.POST.get('description_en', '')
        product.description_ar = request.POST.get('description_ar', '')
        product.price = request.POST.get('price', 0)
        product.old_price = request.POST.get('old_price') or None
        product.is_available = request.POST.get('is_available') == 'on'
        
        product.save()
        
        messages.success(request, 'تم تحديث المنتج بنجاح')
        return redirect('dashboard:product_list')
    
    # GET request
    businesses = request.user.businesses.filter(is_active=True)
    
    context = {
        'product': product,
        'businesses': businesses,
        'is_edit': True,
    }
    
    return render(request, 'dashboard/owner/product_form.html', context)


@require_POST
@business_owner_required
def product_delete(request, slug):
    """حذف منتج"""
    product = get_object_or_404(
        Product,
        slug=slug,
        business__owner=request.user
    )
    
    product.delete()
    messages.success(request, 'تم حذف المنتج بنجاح')
    return redirect('dashboard:product_list')


# ========================================
# Deal Management
# ========================================
@business_owner_required
def deal_list(request):
    """قائمة العروض"""
    from django.utils import timezone
    
    deals = Deal.objects.filter(
        business__owner=request.user
    ).select_related('business')
    
    # فلتر حسب الحالة
    status = request.GET.get('status')
    if status == 'active':
        deals = deals.filter(end_date__gte=timezone.now())
    elif status == 'expired':
        deals = deals.filter(end_date__lt=timezone.now())
    
    context = {
        'deals': deals,
        'status': status,
    }
    
    return render(request, 'dashboard/owner/deal_list.html', context)


@business_owner_required
def deal_create(request):
    """إضافة عرض جديد"""
    if request.method == 'POST':
        deal = Deal(
            business_id=request.POST.get('business'),
            deal_type=request.POST.get('deal_type'),
            title_en=request.POST.get('title_en'),
            title_ar=request.POST.get('title_ar'),
            description_en=request.POST.get('description_en', ''),
            description_ar=request.POST.get('description_ar', ''),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
        )
        
        # حسب نوع العرض
        if deal.deal_type == 'percentage':
            deal.discount_percentage = request.POST.get('discount_percentage')
        elif deal.deal_type == 'fixed':
            deal.original_price = request.POST.get('original_price')
            deal.discounted_price = request.POST.get('discounted_price')
        
        if 'image' in request.FILES:
            deal.image = request.FILES['image']
        
        deal.save()
        
        messages.success(request, 'تم إضافة العرض بنجاح')
        return redirect('dashboard:deal_list')
    
    # GET request
    businesses = request.user.businesses.filter(is_active=True)
    
    context = {
        'businesses': businesses,
    }
    
    return render(request, 'dashboard/owner/deal_form.html', context)


# ========================================
# Review Management
# ========================================
@business_owner_required
def review_list(request):
    """قائمة التعليقات"""
    reviews = Review.objects.filter(
        business__owner=request.user,
        is_approved=True
    ).select_related('business', 'user').order_by('-created_at')
    
    # فلتر حسب الحالة
    status = request.GET.get('status')
    if status == 'pending':
        reviews = reviews.filter(reply__isnull=True)
    elif status == 'replied':
        reviews = reviews.filter(reply__isnull=False)
    
    context = {
        'reviews': reviews,
        'status': status,
    }
    
    return render(request, 'dashboard/owner/review_list.html', context)


@require_POST
@business_owner_required
def review_reply(request, pk):
    """الرد على التعليق"""
    review = get_object_or_404(
        Review,
        pk=pk,
        business__owner=request.user
    )
    
    reply = request.POST.get('reply', '').strip()
    
    if reply:
        review.reply = reply
        review.replied_at = timezone.now()
        review.save()
        
        messages.success(request, 'تم إرسال الرد بنجاح')
    else:
        messages.error(request, 'يجب كتابة الرد')
    
    return redirect('dashboard:review_list')
