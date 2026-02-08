"""
Admin CRUD Views
================
Create, Read, Update, Delete operations for admin
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction

from apps.accounts.models import User
from apps.directory.models import Business
from apps.products.models import Product
from apps.deals.models import Deal
from apps.categories.models import Category

# Import forms from the forms.py file directly
import sys
import os
from importlib import import_module

# Get the forms module
forms_module = import_module('apps.dashboard.forms')

# Try to get the new forms, fallback to creating inline forms
try:
    from django import forms as django_forms
    from django.contrib.auth.forms import UserCreationForm
    
    # Define forms inline if not available
    class AdminUserCreateForm(UserCreationForm):
        email = django_forms.EmailField(required=True)
        first_name = django_forms.CharField(max_length=150, required=False)
        last_name = django_forms.CharField(max_length=150, required=False)
        is_staff = django_forms.BooleanField(required=False, label='مشرف')
        is_active = django_forms.BooleanField(required=False, initial=True, label='فعّال')
        
        class Meta:
            model = User
            fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')

    class AdminUserEditForm(django_forms.ModelForm):
        class Meta:
            model = User
            fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
            widgets = {
                'username': django_forms.TextInput(attrs={'class': 'form-control'}),
                'email': django_forms.EmailInput(attrs={'class': 'form-control'}),
                'first_name': django_forms.TextInput(attrs={'class': 'form-control'}),
                'last_name': django_forms.TextInput(attrs={'class': 'form-control'}),
            }

    class BusinessForm(django_forms.ModelForm):
        class Meta:
            model = Business
            fields = [
                'name_en', 'name_ar', 'description_en', 'description_ar',
                'category', 'business_type', 'email', 'phone', 'whatsapp', 'website',
                'address_ar', 'city_ar', 'district_ar', 'logo', 'cover_image',
                'is_active', 'is_verified', 'is_featured', 'latitude', 'longitude',
            ]
            widgets = {
                'name_en': django_forms.TextInput(attrs={'class': 'form-control'}),
                'name_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
                'description_en': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                'description_ar': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                'category': django_forms.Select(attrs={'class': 'form-select'}),
                'business_type': django_forms.Select(attrs={'class': 'form-select'}),
            }

    class ProductForm(django_forms.ModelForm):
        class Meta:
            model = Product
            fields = [
                'name_en', 'name_ar', 'description_en', 'description_ar',
                'product_type', 'price', 'image', 'is_available', 'is_featured',
            ]
            widgets = {
                'name_en': django_forms.TextInput(attrs={'class': 'form-control'}),
                'name_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
                'product_type': django_forms.Select(attrs={'class': 'form-select'}),
                'price': django_forms.NumberInput(attrs={'class': 'form-control'}),
            }

    class CategoryForm(django_forms.ModelForm):
        class Meta:
            model = Category
            fields = [
                'name_en', 'name_ar', 'description_en', 'description_ar',
                'parent', 'icon', 'image', 'order', 'is_active',
                'meta_keywords_en', 'meta_keywords_ar',
            ]
            widgets = {
                'name_en': django_forms.TextInput(attrs={'class': 'form-control'}),
                'name_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
                'parent': django_forms.Select(attrs={'class': 'form-select'}),
            }

    class DealForm(django_forms.ModelForm):
        class Meta:
            model = Deal
            fields = [
                'title_en', 'title_ar', 'description_en', 'description_ar',
                'deal_type', 'discount_percentage', 'discount_amount',
                'original_price', 'final_price', 'start_date', 'end_date',
                'terms_en', 'terms_ar', 'image', 'max_uses', 'max_uses_per_user',
                'is_active', 'is_featured',
            ]
            widgets = {
                'title_en': django_forms.TextInput(attrs={'class': 'form-control'}),
                'title_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
                'deal_type': django_forms.Select(attrs={'class': 'form-select'}),
                'start_date': django_forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
                'end_date': django_forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            }
except Exception as e:
    print(f"Error loading forms: {e}")


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
            for error in form.errors.values():
                messages.error(request, error)
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
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            messages.success(request, f'تم إضافة المحل {business.name_ar} بنجاح')
            return redirect('admin_dashboard:business_detail', business_id=business.id)
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = BusinessForm()
    
    return render(request, 'dashboard/admin/business_form.html', {'form': form, 'action': 'إضافة'})


@staff_member_required
def admin_business_edit_view(request, business_id):
    """تعديل محل"""
    business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث بيانات المحل بنجاح')
            return redirect('admin_dashboard:business_detail', business_id=business_id)
    else:
        form = BusinessForm(instance=business)
    
    return render(request, 'dashboard/admin/business_form.html', {
        'form': form,
        'business': business,
        'action': 'تعديل'
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
            product = form.save(commit=False)
            if business:
                product.business = business
            product.save()
            messages.success(request, f'تم إضافة المنتج {product.name_ar} بنجاح')
            return redirect('admin_dashboard:product_detail', product_id=product.id)
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
            form.save()
            messages.success(request, 'تم تحديث بيانات المنتج بنجاح')
            return redirect('admin_dashboard:product_detail', product_id=product_id)
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
            category = form.save()
            messages.success(request, f'تم إضافة التصنيف {category.name_ar} بنجاح')
            return redirect('admin_dashboard:categories_list')
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
            form.save()
            messages.success(request, 'تم تحديث بيانات التصنيف بنجاح')
            return redirect('admin_dashboard:categories_list')
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
            deal = form.save(commit=False)
            if business:
                deal.business = business
            deal.save()
            messages.success(request, f'تم إضافة العرض {deal.title_ar} بنجاح')
            return redirect('admin_dashboard:deal_detail', deal_id=deal.id)
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
            form.save()
            messages.success(request, 'تم تحديث بيانات العرض بنجاح')
            return redirect('admin_dashboard:deal_detail', deal_id=deal_id)
    else:
        form = DealForm(instance=deal)
    
    return render(request, 'dashboard/admin/deal_form.html', {
        'form': form,
        'deal': deal,
        'action': 'تعديل'
    })
