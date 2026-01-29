"""
Directory App Models - دليل أي خدمة
=====================================
نماذج قاعدة البيانات الشاملة مع دعم ثنائي اللغة (EN/AR)
"""

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db.models import Count, Q, Avg
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# ========================================
# نموذج المحافظات - Governorate Model
# ========================================
class Governorate(models.Model):
    """نموذج المحافظات المصرية - ثنائي اللغة"""
    
    # English
    name_en = models.CharField(
        max_length=100,
        verbose_name='Name (English)',
        db_index=True,
        help_text='Example: Ismailia, Cairo, Alexandria'
    )
    
    # Arabic
    name_ar = models.CharField(
        max_length=100,
        verbose_name='الاسم بالعربية',
        db_index=True,
        help_text='مثال: الإسماعيلية، القاهرة، الإسكندرية'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL Slug'
    )
    
    # Description (bilingual)
    description_en = models.TextField(
        blank=True,
        verbose_name='Description (English)',
        help_text='Brief description about the governorate'
    )
    description_ar = models.TextField(
        blank=True,
        verbose_name='الوصف بالعربية',
        help_text='وصف مختصر عن المحافظة'
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='fas fa-city',
        verbose_name='Font Awesome Icon',
        help_text='Example: fas fa-city, fas fa-building'
    )
    
    image = models.ImageField(
        upload_to='governorates/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Governorate Image',
        help_text='Representative image for the governorate'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text='Deactivating hides the governorate from the site'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='Display Order',
        help_text='Lower number = displayed first',
        validators=[MinValueValidator(0)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    
    class Meta:
        verbose_name = 'Governorate'
        verbose_name_plural = 'Governorates'
        ordering = ['order', 'name_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['name_en']),
            models.Index(fields=['name_ar']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['name_en'],
                name='unique_governorate_name_en'
            ),
            models.UniqueConstraint(
                fields=['name_ar'],
                name='unique_governorate_name_ar'
            ),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name_en} / {self.name_ar}"
    
    @property
    def name(self):
        """Get name based on current language"""
        from django.utils.translation import get_language
        lang = get_language()
        return self.name_ar if lang == 'ar' else self.name_en
    
    @property
    def description(self):
        """Get description based on current language"""
        from django.utils.translation import get_language
        lang = get_language()
        return self.description_ar if lang == 'ar' else self.description_en
    
    def get_absolute_url(self):
        return reverse('directory:governorate_detail', kwargs={'slug': self.slug})
    
    def get_business_count(self):
        """عدد المحلات النشطة والموثقة في المحافظة"""
        return self.cities.filter(
            is_active=True
        ).aggregate(
            count=Count(
                'districts__businesses',
                filter=Q(
                    districts__businesses__is_active=True,
                    districts__businesses__is_verified=True
                ),
                distinct=True
            )
        )['count'] or 0
    
    def get_cities_count(self):
        """عدد المدن النشطة في المحافظة"""
        return self.cities.filter(is_active=True).count()
    
    def get_districts_count(self):
        """عدد الأحياء النشطة في المحافظة"""
        return District.objects.filter(
            city__governorate=self,
            is_active=True
        ).count()


# ========================================
# نموذج المدن - City Model
# ========================================
class City(models.Model):
    """نموذج المدن - المستوى الثاني للمواقع الجغرافية"""
    
    governorate = models.ForeignKey(
        Governorate,
        on_delete=models.CASCADE,
        related_name='cities',
        related_query_name='city',
        verbose_name='Governorate'
    )
    
    name_en = models.CharField(
        max_length=100,
        verbose_name='City Name (English)',
        db_index=True,
        help_text='Example: Ismailia City, Fayed, Qantara'
    )
    
    name_ar = models.CharField(
        max_length=100,
        verbose_name='اسم المدينة',
        db_index=True,
        help_text='مثال: مدينة الإسماعيلية، فايد، القنطرة'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL Slug'
    )
    
    description_en = models.TextField(
        blank=True,
        verbose_name='Description (English)'
    )
    
    description_ar = models.TextField(
        blank=True,
        verbose_name='الوصف'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='Display Order',
        validators=[MinValueValidator(0)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['governorate__order', 'order', 'name_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['governorate', 'is_active']),
            models.Index(fields=['is_active', 'order']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['governorate', 'name_en'],
                name='unique_city_name_en_per_governorate'
            ),
            models.UniqueConstraint(
                fields=['governorate', 'name_ar'],
                name='unique_city_name_ar_per_governorate'
            ),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.governorate.name_en}-{self.name_en}")
            slug = base_slug
            counter = 1
            while City.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name_en} / {self.name_ar} - {self.governorate.name_en}"
    
    @property
    def name(self):
        from django.utils.translation import get_language
        lang = get_language()
        return self.name_ar if lang == 'ar' else self.name_en
    
    @property
    def description(self):
        from django.utils.translation import get_language
        lang = get_language()
        return self.description_ar if lang == 'ar' else self.description_en
    
    def get_absolute_url(self):
        return reverse('directory:city_detail', kwargs={'slug': self.slug})
    
    def get_business_count(self):
        """عدد المحلات النشطة في المدينة"""
        return Business.objects.filter(
            district__city=self,
            is_active=True,
            is_verified=True
        ).count()
    
    def get_districts_count(self):
        """عدد الأحياء النشطة في المدينة"""
        return self.districts.filter(is_active=True).count()


# ========================================
# نموذج الأحياء - District Model
# ========================================
class District(models.Model):
    """نموذج الأحياء - المستوى الثالث للمواقع الجغرافية"""
    
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='districts',
        related_query_name='district',
        verbose_name='City'
    )
    
    name_en = models.CharField(
        max_length=100,
        verbose_name='District Name (English)',
        db_index=True,
        help_text='Example: El Sheikh Zayed, El Taawon, El Afrang'
    )
    
    name_ar = models.CharField(
        max_length=100,
        verbose_name='اسم الحي',
        db_index=True,
        help_text='مثال: الشيخ زايد، التعاون، الأفرنج'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL Slug'
    )
    
    description_en = models.TextField(
        blank=True,
        verbose_name='Description (English)'
    )
    
    description_ar = models.TextField(
        blank=True,
        verbose_name='الوصف'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='Display Order',
        validators=[MinValueValidator(0)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    
    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        ordering = ['city__order', 'order', 'name_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['city', 'is_active']),
            models.Index(fields=['is_active', 'order']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['city', 'name_en'],
                name='unique_district_name_en_per_city'
            ),
            models.UniqueConstraint(
                fields=['city', 'name_ar'],
                name='unique_district_name_ar_per_city'
            ),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.city.governorate.name_en}-{self.city.name_en}-{self.name_en}")
            slug = base_slug
            counter = 1
            while District.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name_en} / {self.name_ar} - {self.city.name_en}"
    
    @property
    def name(self):
        from django.utils.translation import get_language
        lang = get_language()
        return self.name_ar if lang == 'ar' else self.name_en
    
    @property
    def governorate(self):
        """الحصول على المحافظة"""
        return self.city.governorate
    
    def get_absolute_url(self):
        return reverse('directory:district_detail', kwargs={'slug': self.slug})
    
    def get_business_count(self):
        """عدد المحلات النشطة في الحي"""
        return self.businesses.filter(
            is_active=True,
            is_verified=True
        ).count()


# ========================================
# نموذج الفئات - Category Model
# ========================================
class Category(models.Model):
    """نموذج الفئات - ثنائي اللغة مع دعم الفئات الفرعية"""
    
    # Parent category for hierarchical structure
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        related_query_name='child',
        null=True,
        blank=True,
        verbose_name='Parent Category',
        help_text='Leave empty for main category'
    )
    
    # English
    name_en = models.CharField(
        max_length=100,
        verbose_name='Category Name (English)',
        db_index=True,
        help_text='Example: Restaurants, Medical, Shopping'
    )
    
    # Arabic
    name_ar = models.CharField(
        max_length=100,
        verbose_name='اسم الفئة',
        db_index=True,
        help_text='مثال: مطاعم ومقاهي، طبية، تسوق'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL Slug'
    )
    
    # Description (bilingual)
    description_en = models.TextField(
        blank=True,
        verbose_name='Description (English)'
    )
    description_ar = models.TextField(
        blank=True,
        verbose_name='الوصف بالعربية'
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='fas fa-store',
        verbose_name='Font Awesome Icon',
        help_text='Example: fas fa-utensils, fas fa-hospital'
    )
    
    image = models.ImageField(
        upload_to='categories/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Category Image'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='Display Order',
        validators=[MinValueValidator(0)]
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    
    # SEO
    meta_keywords_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Meta Keywords (English)',
        help_text='Comma-separated keywords for SEO'
    )
    meta_keywords_ar = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='الكلمات المفتاحية',
        help_text='كلمات مفتاحية للسيو مفصولة بفاصلة'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['parent__order', 'order', 'name_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent', 'is_active']),
            models.Index(fields=['is_active', 'order']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            if self.parent:
                base_slug = slugify(f"{self.parent.name_en}-{self.name_en}")
            else:
                base_slug = slugify(self.name_en)
            
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name_en} > {self.name_en} / {self.name_ar}"
        return f"{self.name_en} / {self.name_ar}"
    
    @property
    def name(self):
        from django.utils.translation import get_language
        lang = get_language()
        return self.name_ar if lang == 'ar' else self.name_en
    
    @property
    def description(self):
        from django.utils.translation import get_language
        lang = get_language()
        return self.description_ar if lang == 'ar' else self.description_en
    
    def get_absolute_url(self):
        return reverse('directory:category_detail', kwargs={'slug': self.slug})
    
    def get_business_count(self):
        """عدد المحلات النشطة في الفئة"""
        return self.businesses.filter(
            is_active=True,
            is_verified=True
        ).count()
    
    def get_all_business_count(self):
        """عدد المحلات في الفئة وجميع الفئات الفرعية"""
        categories = [self] + list(self.children.filter(is_active=True))
        return Business.objects.filter(
            category__in=categories,
            is_active=True,
            is_verified=True
        ).count()


# يتبع في الرسالة القادمة... 🚀
