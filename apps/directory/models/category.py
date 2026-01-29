"""
Category Model - نموذج الفئات
============================
دعم الفئات الرئيسية والفرعية - ثنائي اللغة
"""

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse


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
        help_text='كلمات مفتاحية للسيو'
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
        from .business import Business
        return Business.objects.filter(
            category=self,
            is_active=True,
            is_verified=True
        ).count()
    
    def get_all_business_count(self):
        """عدد المحلات في الفئة وجميع الفئات الفرعية"""
        from .business import Business
        categories = [self] + list(self.children.filter(is_active=True))
        return Business.objects.filter(
            category__in=categories,
            is_active=True,
            is_verified=True
        ).count()
