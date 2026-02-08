"""
Admin CRUD Views
================
Create, Read, Update, Delete operations for admin
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction
from django import forms as django_forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import User
from apps.directory.models import Business
from apps.products.models import Product
from apps.deals.models import Deal
from apps.categories.models import Category


# ========================================
# FORM DEFINITIONS
# ========================================

class AdminUserCreateForm(UserCreationForm):
    """Form for creating users by admin"""
    email = django_forms.EmailField(required=True)
    first_name = django_forms.CharField(max_length=150, required=False)
    last_name = django_forms.CharField(max_length=150, required=False)
    is_staff = django_forms.BooleanField(required=False, label='مشرف')
    is_active = django_forms.BooleanField(required=False, initial=True, label='فعّال')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')


class AdminUserEditForm(django_forms.ModelForm):
    """Form for editing users by admin"""
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
    """Form for creating/editing businesses"""
    class Meta:
        model = Business
        exclude = ('owner', 'created_at', 'updated_at', 'slug', 'views_count', 'clicks_count')
        widgets = {
            'name_en': django_forms.TextInput(attrs={'class': 'form-control'}),
            'name_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
            'description_en': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_ar': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': django_forms.Select(attrs={'class': 'form-select'}),
            'business_type': django_forms.Select(attrs={'class': 'form-select'}),
        }


class ProductForm(django_forms.ModelForm):
    """Form for creating/editing products"""
    class Meta:
        model = Product
        exclude = ('business', 'created_at', 'updated_at', 'slug')
        widgets = {
            'name_en': django_forms.TextInput(attrs={'class': 'form-control'}),
            'name_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
            'description_en': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_ar': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'product_type': django_forms.Select(attrs={'class': 'form-select'}),
            'price': django_forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class CategoryForm(django_forms.ModelForm):
    """Form for creating/editing categories"""
    class Meta:
        model = Category
        exclude = ('created_at', 'updated_at', 'slug')
        widgets = {
            'name_en': django_forms.TextInput(attrs={'class': 'form-control'}),
            'name_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
            'description_en': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description_ar': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': django_forms.Select(attrs={'class': 'form-select'}),
            'icon': django_forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-store'}),
        }


class DealForm(django_forms.ModelForm):
    """Form for creating/editing deals"""
    class Meta:
        model = Deal
        exclude = ('business', 'created_at', 'updated_at', 'slug', 'used_count')
        widgets = {
            'title_en': django_forms.TextInput(attrs={'class': 'form-control'}),
            'title_ar': django_forms.TextInput(attrs={'class': 'form-control'}),
            'description_en': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_ar': django_forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'deal_type': django_forms.Select(attrs={'class': 'form-select'}),
            'start_date': django_forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': django_forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


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
