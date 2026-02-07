"""
Product Management Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from apps.products.models import Product
from apps.directory.models import Business
from apps.dashboard.forms import ProductForm


@login_required
def product_list(request):
    """قائمة منتجات المستخدم"""
    products = Product.objects.filter(
        business__owner=request.user
    ).select_related('business').order_by('-created_at')
    
    # Filter by business
    business_id = request.GET.get('business')
    if business_id:
        products = products.filter(business_id=business_id)
    
    # Filter by type
    product_type = request.GET.get('type')
    if product_type:
        products = products.filter(product_type=product_type)
    
    # Filter by status (availability)
    status = request.GET.get('status')
    if status == 'available':
        products = products.filter(is_available=True)
    elif status == 'unavailable':
        products = products.filter(is_available=False)
    
    # Search
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name_en__icontains=search) |
            Q(name_ar__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    # Get user businesses for filter
    businesses = Business.objects.filter(owner=request.user)
    
    # Calculate statistics
    all_products = Product.objects.filter(business__owner=request.user)
    
    context = {
        'products': products,
        'businesses': businesses,
        'total_count': all_products.count(),
        'available_count': all_products.filter(is_available=True).count(),
        'products_count': all_products.filter(product_type='product').count(),
        'services_count': all_products.filter(product_type='service').count(),
    }
    
    return render(request, 'dashboard/product/list.html', context)


@login_required
def product_create(request):
    """إضافة منتج جديد"""
    # Get user businesses
    user_businesses = Business.objects.filter(owner=request.user)
    
    if not user_businesses.exists():
        messages.warning(request, 'يجب إضافة محل أولاً قبل إضافة منتجات!')
        return redirect('dashboard:business_create')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'تم إضافة المنتج بنجاح!')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'إضافة منتج جديد',
    }
    
    return render(request, 'dashboard/product/form.html', context)


@login_required
def product_update(request, slug):
    """تعديل منتج"""
    product = get_object_or_404(Product, slug=slug, business__owner=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المنتج بنجاح!')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product, user=request.user)
    
    context = {
        'form': form,
        'product': product,
        'title': f'تعديل {product.name_ar}',
    }
    
    return render(request, 'dashboard/product/form.html', context)


@login_required
def product_delete(request, slug):
    """حذف منتج"""
    product = get_object_or_404(Product, slug=slug, business__owner=request.user)
    
    if request.method == 'POST':
        product_name = product.name_ar
        product.delete()
        messages.success(request, f'تم حذف {product_name} بنجاح!')
        return redirect('dashboard:product_list')
    
    context = {
        'product': product,
    }
    
    return render(request, 'dashboard/product/delete.html', context)
