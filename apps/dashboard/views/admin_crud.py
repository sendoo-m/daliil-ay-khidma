"""
Admin CRUD Views
================
Create, Read, Update, Delete operations for admin
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.directory.models import Business
from apps.products.models import Product
from apps.deals.models import Deal
from apps.categories.models import Category
from apps.directory.models.location import Governorate, City, District

from apps.dashboard.forms import (
    AdminUserCreateForm, AdminUserEditForm, 
    BusinessForm, ProductForm, CategoryForm, DealForm
)

# ========================================
# USER CRUD
# ========================================

@staff_member_required
def admin_user_create(request):
    """إضافة مستخدم جديد"""
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'تم إضافة المستخدم {user.username} بنجاح')
            return redirect('admin_dashboard:user_detail', user_id=user.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = AdminUserCreateForm()
    
    return render(request, 'dashboard/admin/user_form.html', {'form': form, 'action': 'إضافة'})

@staff_member_required
def admin_user_edit_view(request, user_id):
    """تعديل مستخدم"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث بيانات المستخدم بنجاح')
            return redirect('admin_dashboard:user_detail', user_id=user_id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = AdminUserEditForm(instance=user)
    
    return render(request, 'dashboard/admin/user_form.html', {
        'form': form,
        'user_obj': user,
        'action': 'تعديل'
    })

# ========================================
# BUSINESS CRUD
# ========================================

@staff_member_required
def admin_business_create(request):
    """إضافة محل جديد"""
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                business = form.save(commit=False)
                business.owner = request.user
                business.save()
                messages.success(request, f'✅ تم إضافة المحل "{business.name_ar}" بنجاح!')
                return redirect('admin_dashboard:business_detail', business_id=business.id)
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء حفظ المحل: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = BusinessForm()
    
    governorates = Governorate.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    return render(request, 'dashboard/admin/business_form.html', {
        'form': form, 
        'action': 'إضافة',
        'title': 'إضافة محل جديد',
        'governorates': governorates,
        'categories': categories
    })

@staff_member_required
def admin_business_edit_view(request, business_id):
    """تعديل محل"""
    business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'✅ تم تحديث بيانات المحل "{business.name_ar}" بنجاح!')
                return redirect('admin_dashboard:business_detail', business_id=business_id)
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء التحديث: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = BusinessForm(instance=business)
    
    governorates = Governorate.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    return render(request, 'dashboard/admin/business_form.html', {
        'form': form,
        'business': business,
        'action': 'تعديل',
        'title': f'تعديل محل: {business.name_ar}',
        'governorates': governorates,
        'categories': categories
    })

# ========================================
# PRODUCT CRUD
# ========================================

@staff_member_required
def admin_product_create(request, business_id=None):
    """إضافة منتج جديد"""
    business = None
    if business_id:
        business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                if business:
                    product.business = business
                elif not product.business:
                    messages.error(request, '❌ يجب تحديد المحل التابع له المنتج')
                    return render(request, 'dashboard/admin/product_form.html', {
                        'form': form,
                        'business': business,
                        'action': 'إضافة'
                    })
                product.save()
                messages.success(request, f'✅ تم إضافة المنتج "{product.name_ar}" بنجاح!')
                return redirect('admin_dashboard:product_detail', product_id=product.id)
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء حفظ المنتج: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = ProductForm()
    
    return render(request, 'dashboard/admin/product_form.html', {
        'form': form,
        'business': business,
        'action': 'إضافة'
    })

@staff_member_required
def admin_product_edit_view(request, product_id):
    """تعديل منتج"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'✅ تم تحديث بيانات المنتج "{product.name_ar}" بنجاح!')
                return redirect('admin_dashboard:product_detail', product_id=product_id)
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء التحديث: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'dashboard/admin/product_form.html', {
        'form': form,
        'product': product,
        'action': 'تعديل'
    })

# ========================================
# CATEGORY CRUD
# ========================================

@staff_member_required
def admin_category_create_view(request):
    """إضافة تصنيف جديد"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                category = form.save()
                messages.success(request, f'✅ تم إضافة التصنيف "{category.name_ar}" بنجاح!')
                return redirect('admin_dashboard:categories_list')
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء حفظ التصنيف: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/admin/category_form.html', {'form': form, 'action': 'إضافة'})

@staff_member_required
def admin_category_edit_view(request, category_id):
    """تعديل تصنيف"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'✅ تم تحديث بيانات التصنيف "{category.name_ar}" بنجاح!')
                return redirect('admin_dashboard:categories_list')
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء التحديث: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'dashboard/admin/category_form.html', {
        'form': form,
        'category': category,
        'action': 'تعديل'
    })

# ========================================
# DEAL CRUD
# ========================================

@staff_member_required
def admin_deal_create(request, business_id=None):
    """إضافة عرض جديد"""
    business = None
    if business_id:
        business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        form = DealForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                deal = form.save(commit=False)
                if business:
                    deal.business = business
                elif not deal.business:
                    messages.error(request, '❌ يجب تحديد المحل التابع له العرض')
                    return render(request, 'dashboard/admin/deal_form.html', {
                        'form': form,
                        'business': business,
                        'action': 'إضافة'
                    })
                deal.save()
                messages.success(request, f'✅ تم إضافة العرض "{deal.title_ar}" بنجاح!')
                return redirect('admin_dashboard:deal_detail', deal_id=deal.id)
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء حفظ العرض: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = DealForm()
    
    return render(request, 'dashboard/admin/deal_form.html', {
        'form': form,
        'business': business,
        'action': 'إضافة'
    })

@staff_member_required
def admin_deal_edit_view(request, deal_id):
    """تعديل عرض"""
    deal = get_object_or_404(Deal, id=deal_id)
    
    if request.method == 'POST':
        form = DealForm(request.POST, request.FILES, instance=deal)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'✅ تم تحديث بيانات العرض "{deal.title_ar}" بنجاح!')
                return redirect('admin_dashboard:deal_detail', deal_id=deal_id)
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء التحديث: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'خطأ في {field}: {error}')
    else:
        form = DealForm(instance=deal)
    
    return render(request, 'dashboard/admin/deal_form.html', {
        'form': form,
        'deal': deal,
        'action': 'تعديل'
    })


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.directory.models import District  # عدل المسار حسب موديلك

@login_required
def ajax_get_districts(request):
    governorate_id = request.GET.get('governorate_id')
    results = []

    if governorate_id:
        districts = District.objects.filter(city__governorate_id=governorate_id).order_by('name_ar')
        results = [
            {
                "id": d.id,
                "text": d.name_ar,  # أو name_en حسب ما تعرضه
            }
            for d in districts
        ]

    return JsonResponse({"results": results})
