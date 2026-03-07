"""
Business Management Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from apps.directory.models import Business
from apps.dashboard.forms import BusinessForm


@login_required
def business_list(request):
    """قائمة محلات المستخدم"""
    businesses = Business.objects.filter(
        owner=request.user
    ).select_related(
        'category', 'district__city__governorate'
    ).order_by('-created_at')
    
    # Filter by type
    business_type = request.GET.get('type')
    if business_type:
        businesses = businesses.filter(business_type=business_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'active':
        businesses = businesses.filter(is_active=True)
    elif status == 'inactive':
        businesses = businesses.filter(is_active=False)
    elif status == 'verified':
        businesses = businesses.filter(is_verified=True)
    
    # Search
    search = request.GET.get('search')
    if search:
        businesses = businesses.filter(
            models.Q(name_en__icontains=search) |
            models.Q(name_ar__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(businesses, 10)
    page = request.GET.get('page')
    businesses = paginator.get_page(page)
    
    context = {
        'businesses': businesses,
        'total_count': Business.objects.filter(owner=request.user).count(),
        'active_count': Business.objects.filter(owner=request.user, is_active=True).count(),
        'verified_count': Business.objects.filter(owner=request.user, is_verified=True).count(),
    }
    
    return render(request, 'dashboard/business/list.html', context)

from apps.dashboard.forms.business_create import BusinessCreateForm, BusinessImageFormSet
from apps.directory.models.location import Governorate


@login_required
def business_create(request, business_type='shop'):
    """إنشاء محل جديد - shop أو craft"""

    # التحقق من النوع
    if business_type not in ['shop', 'craft']:
        return redirect('dashboard:business_list')

    # العناوين حسب النوع
    titles = {
        'shop':  {'ar': 'إضافة محل تجاري جديد',    'icon': '🏪'},
        'craft': {'ar': 'إضافة حرفة / مهنة حرة',   'icon': '🔧'},
    }

    if request.method == 'POST':
        form     = BusinessCreateForm(request.POST, request.FILES,
                                      business_type=business_type, user=request.user)
        formset  = BusinessImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            business              = form.save(commit=False)
            business.owner        = request.user
            business.business_type = business_type
            business.save()

            # حفظ الصور
            formset.instance = business
            formset.save()

            messages.success(request, f'✅ تم إضافة "{business.name_ar}" بنجاح!')
            return redirect('dashboard:business_detail', slug=business.slug)
    else:
        form    = BusinessCreateForm(business_type=business_type, user=request.user)
        formset = BusinessImageFormSet()

    return render(request, 'dashboard/business/form.html', {
        'form':          form,
        'formset':       formset,
        'business_type': business_type,
        'title':         titles[business_type],
        'governorates':  Governorate.objects.filter(is_active=True).order_by('name_ar'),
        'action':        'create',
    })


@login_required
def business_update(request, slug):
    """تعديل محل"""
    business = get_object_or_404(Business, slug=slug, owner=request.user)

    if request.method == 'POST':
        form    = BusinessCreateForm(request.POST, request.FILES,
                                     instance=business, user=request.user)
        formset = BusinessImageFormSet(request.POST, request.FILES, instance=business)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'✅ تم تحديث "{business.name_ar}" بنجاح!')
            return redirect('dashboard:business_detail', slug=business.slug)
    else:
        form    = BusinessCreateForm(instance=business, user=request.user)
        formset = BusinessImageFormSet(instance=business)

    return render(request, 'dashboard/business/form.html', {
        'form':          form,
        'formset':       formset,
        'business':      business,
        'business_type': business.business_type,
        'title':         {'ar': f'تعديل: {business.name_ar}', 'icon': '✏️'},
        'governorates':  Governorate.objects.filter(is_active=True).order_by('name_ar'),
        'action':        'update',
    })

# @login_required
# def business_create(request):
#     """إضافة محل جديد"""
#     if request.method == 'POST':
#         form = BusinessForm(request.POST, request.FILES)
#         if form.is_valid():
#             business = form.save(commit=False)
#             business.owner = request.user
#             business.save()
#             messages.success(request, 'تم إضافة المحل بنجاح!')
#             return redirect('dashboard:business_detail', slug=business.slug)
#     else:
#         form = BusinessForm()
    
#     context = {
#         'form': form,
#         'title': 'إضانفة محل جديد',
#     }
    
#     return render(request, 'dashboard/business/form.html', context)


# @login_required
# def business_update(request, slug):
#     """تعديل محل"""
#     business = get_object_or_404(Business, slug=slug, owner=request.user)
    
#     if request.method == 'POST':
#         form = BusinessForm(request.POST, request.FILES, instance=business)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'تم تحديث المحل بنجاح!')
#             return redirect('dashboard:business_detail', slug=business.slug)
#     else:
#         form = BusinessForm(instance=business)
    
#     context = {
#         'form': form,
#         'business': business,
#         'title': f'تعديل {business.name_ar}',
#     }
    
#     return render(request, 'dashboard/business/form.html', context)


@login_required
def business_detail(request, slug):
    """تفاصيل المحل"""
    business = get_object_or_404(
        Business.objects.select_related(
            'category', 'district__city__governorate'
        ).prefetch_related('images'),
        slug=slug,
        owner=request.user
    )
    
    # Get business products
    from apps.products.models import Product
    products = Product.objects.filter(business=business)[:5]
    
    # Get business deals
    from apps.deals.models import Deal
    deals = Deal.objects.filter(business=business)[:5]
    
    context = {
        'business': business,
        'products': products,
        'deals': deals,
    }
    
    return render(request, 'dashboard/business/detail.html', context)


@login_required
def business_delete(request, slug):
    """حذف محل"""
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        business_name = business.name_ar
        business.delete()
        messages.success(request, f'تم حذف {business_name} بنجاح!')
        return redirect('dashboard:business_list')
    
    context = {
        'business': business,
    }
    
    return render(request, 'dashboard/business/delete.html', context)
