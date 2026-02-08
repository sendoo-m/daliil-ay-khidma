"""
Dashboard Forms
===============
Forms for admin and owner dashboards
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User
from apps.directory.models import Business
from apps.directory.models.location import Governorate, District
from apps.products.models import Product
from apps.deals.models import Deal
from apps.categories.models import Category


# ========================================
# USER FORMS
# ========================================
class AdminUserCreateForm(UserCreationForm):
    """Form for creating users by admin"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    is_staff = forms.BooleanField(required=False, label='مشرف')
    is_active = forms.BooleanField(required=False, initial=True, label='فعّال')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')


class AdminUserEditForm(forms.ModelForm):
    """Form for editing users by admin"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ========================================
# BUSINESS FORMS
# ========================================
class BusinessForm(forms.ModelForm):
    """Form for creating/editing businesses"""
    
    # Add custom governorate field for better UX (NOT saved to DB)
    governorate = forms.ModelChoiceField(
        queryset=Governorate.objects.filter(is_active=True).order_by('order', 'name_ar'),
        required=False,
        label='المحافظة',
        widget=forms.Select(attrs={'class': 'form-select select2-dropdown'}),
        help_text='اختر المحافظة أولاً'
    )
    
    class Meta:
        model = Business
        fields = [
            'name_en', 'name_ar',
            'description_en', 'description_ar',
            'category',
            'business_type',
            'district',
            'email', 'phone', 'whatsapp', 'website',
            'address_ar', 'address_en',
            'logo', 'cover_image',
            'is_active', 'is_verified', 'is_featured',
            'latitude', 'longitude',
            'working_hours_ar', 'working_hours_en',
            'facebook', 'instagram', 'twitter', 'tiktok',
            'location_url',
        ]
        widgets = {
            'name_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}),
            'name_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المحل'}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select select2-dropdown'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'class': 'form-select select2-dropdown'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'العنوان بالتفصيل'}),
            'address_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detailed address'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'working_hours_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 9 صباحاً - 10 مساءً'}),
            'working_hours_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: 9 AM - 10 PM'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/...'}),
            'tiktok': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://tiktok.com/@...'}),
            'location_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Google Maps Link'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing existing business, set the governorate
        if self.instance.pk and self.instance.district:
            self.fields['governorate'].initial = self.instance.district.city.governorate
    
    def save(self, commit=True):
        # Don't save governorate (it's just a helper field)
        # The district field already contains all location data
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


# ========================================
# PRODUCT FORMS
# ========================================
class ProductForm(forms.ModelForm):
    """Form for creating/editing products"""
    
    class Meta:
        model = Product
        fields = [
            'name_en', 'name_ar',
            'description_en', 'description_ar',
            'product_type',
            'price',
            'image',
            'is_available', 'is_featured',
        ]
        widgets = {
            'name_en': forms.TextInput(attrs={'class': 'form-control'}),
            'name_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


# ========================================
# CATEGORY FORMS
# ========================================
class CategoryForm(forms.ModelForm):
    """Form for creating/editing categories"""
    
    class Meta:
        model = Category
        fields = [
            'name_en', 'name_ar',
            'description_en', 'description_ar',
            'parent',
            'icon', 'image',
            'order', 'is_active',
            'meta_keywords_en', 'meta_keywords_ar',
        ]
        widgets = {
            'name_en': forms.TextInput(attrs={'class': 'form-control'}),
            'name_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-store'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'meta_keywords_en': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_keywords_ar': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ========================================
# DEAL FORMS
# ========================================
class DealForm(forms.ModelForm):
    """Form for creating/editing deals"""
    
    class Meta:
        model = Deal
        fields = [
            'title_en', 'title_ar',
            'description_en', 'description_ar',
            'deal_type',
            'discount_percentage', 'discount_amount',
            'original_price', 'final_price',
            'start_date', 'end_date',
            'terms_en', 'terms_ar',
            'image',
            'max_uses', 'max_uses_per_user',
            'is_active', 'is_featured',
        ]
        widgets = {
            'title_en': forms.TextInput(attrs={'class': 'form-control'}),
            'title_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'deal_type': forms.Select(attrs={'class': 'form-select'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'original_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'final_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'terms_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'terms_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'max_uses': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_uses_per_user': forms.NumberInput(attrs={'class': 'form-control'}),
        }
