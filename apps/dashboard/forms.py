"""
Dashboard Forms
===============
Forms for admin and owner dashboards
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User
from apps.directory.models import Business
from apps.directory.models.location import Governorate, District, City
from apps.products.models import Product
from apps.deals.models import Deal
from apps.categories.models import Category

# ========================================
# USER FORMS
# ========================================

class UserProfileForm(forms.ModelForm):
    """Form for users to update their own profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الأول'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم العائلة'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
        }

class AdminUserCreateForm(UserCreationForm):
    """Form for creating users by admin"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    is_staff = forms.BooleanField(required=False, label='مشرف')
    is_active = forms.BooleanField(required=False, initial=True, label='فعّال')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

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
    """Form for creating/editing businesses with cascading locations"""
    
    governorate = forms.ModelChoiceField(
        queryset=Governorate.objects.filter(is_active=True).order_by('order', 'name_ar'),
        required=False,
        label='المحافظة',
        widget=forms.Select(attrs={'class': 'form-select select2', 'id': 'id_governorate'}),
        help_text='اختر المحافظة'
    )
    
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        label='المدينة',
        widget=forms.Select(attrs={'class': 'form-select select2', 'id': 'id_city'}),
        help_text='اختر المدينة'
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
            'category': forms.Select(attrs={'class': 'form-select select2'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'class': 'form-select select2', 'id': 'id_district'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'العنوان بالتفصيل'}),
            'address_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detailed address'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'working_hours_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'working_hours_en': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'tiktok': forms.URLInput(attrs={'class': 'form-control'}),
            'location_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Handle initial values and querysets for cascading fields
        if self.instance.pk and self.instance.district:
            try:
                district = self.instance.district
                city = district.city
                gov = city.governorate
                
                self.fields['governorate'].initial = gov
                self.fields['city'].initial = city
                
                # Update querysets based on selection
                self.fields['city'].queryset = City.objects.filter(governorate=gov, is_active=True).order_by('name_ar')
                self.fields['district'].queryset = District.objects.filter(city=city, is_active=True).order_by('name_ar')
            except AttributeError:
                pass
        
        # If form is bound (POST), update querysets from data
        if self.is_bound:
            if self.data.get('governorate'):
                try:
                    gov_id = int(self.data.get('governorate'))
                    self.fields['city'].queryset = City.objects.filter(governorate_id=gov_id, is_active=True).order_by('name_ar')
                except (ValueError, TypeError):
                    pass
            
            if self.data.get('city'):
                try:
                    city_id = int(self.data.get('city'))
                    self.fields['district'].queryset = District.objects.filter(city_id=city_id, is_active=True).order_by('name_ar')
                except (ValueError, TypeError):
                    pass

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
