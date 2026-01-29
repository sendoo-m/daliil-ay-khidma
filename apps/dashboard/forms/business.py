"""
Business Form
"""

from django import forms
from apps.directory.models import Business, BusinessImage


class BusinessForm(forms.ModelForm):
    """Business Creation/Update Form"""
    
    class Meta:
        model = Business
        fields = [
            'business_type',
            'name_en', 'name_ar',
            'category', 'district',
            'logo', 'cover_image',
            'phone', 'whatsapp', 'email', 'website',
            'facebook', 'instagram', 'twitter', 'tiktok',
            'address_en', 'address_ar',
            'location_url', 'latitude', 'longitude',
            'description_en', 'description_ar',
            'working_hours_en', 'working_hours_ar',
        ]
        
        widgets = {
            'business_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Business name in English'
            }),
            'name_ar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المحل بالعربية',
                'dir': 'rtl'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01234567890'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01234567890'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/page'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/profile'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/profile'
            }),
            'tiktok': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://tiktok.com/@profile'
            }),
            'address_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detailed address in English'
            }),
            'address_ar': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'العنوان بالتفصيل',
                'dir': 'rtl'
            }),
            'location_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Google Maps link'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
            'description_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed description about your business'
            }),
            'description_ar': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'وصف تفصيلي عن محلك',
                'dir': 'rtl'
            }),
            'working_hours_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Sat-Thu: 9 AM - 10 PM | Fri: 2 PM - 10 PM'
            }),
            'working_hours_ar': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'السبت-الخميس: 9 ص-10 م | الجمعة: 2 م-10 م',
                'dir': 'rtl'
            }),
        }
        
        labels = {
            'business_type': 'نوع المحل',
            'name_en': 'Business Name (English)',
            'name_ar': 'اسم المحل',
            'category': 'التصنيف',
            'district': 'الحي',
            'logo': 'اللوجو',
            'cover_image': 'صورة الغلاف',
            'phone': 'رقم الهاتف',
            'whatsapp': 'واتساب',
            'email': 'البريد الإلكتروني',
            'website': 'الموقع',
            'address_en': 'Address (English)',
            'address_ar': 'العنوان',
            'description_en': 'Description (English)',
            'description_ar': 'الوصف',
            'working_hours_en': 'Working Hours (English)',
            'working_hours_ar': 'ساعات العمل',
        }
