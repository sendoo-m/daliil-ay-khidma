"""
Location Models - نماذج المواقع الجغرافية
=====================================
Governorate > City > District (3 levels)
"""

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models import Count, Q


class Governorate(models.Model):
    """نموذج المحافظات المصرية - ثنائي اللغة"""
    
    name_en = models.CharField(
        max_length=100,
        verbose_name='Name (English)',
        db_index=True,
        help_text='Example: Ismailia, Cairo, Alexandria'
    )
    
    name_ar = models.CharField(
        max_length=100,
        verbose_name='الاسم بالعربية',
        db_index=True,
        help_text='مثال: الإسماعيلية، القاهرة، الإسكندرية'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )
    
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='fas fa-city'
    )
    
    image = models.ImageField(
        upload_to='governorates/%Y/%m/',
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Governorate'
        verbose_name_plural = 'Governorates'
        ordering = ['order', 'name_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
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
        from django.utils.translation import get_language
        return self.name_ar if get_language() == 'ar' else self.name_en
    
    def get_absolute_url(self):
        return reverse('directory:governorate_detail', kwargs={'slug': self.slug})


class City(models.Model):
    """نموذج المدن"""
    
    governorate = models.ForeignKey(
        Governorate,
        on_delete=models.CASCADE,
        related_name='cities'
    )
    
    name_en = models.CharField(max_length=100, db_index=True)
    name_ar = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['governorate__order', 'order', 'name_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['governorate', 'is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['governorate', 'name_en'],
                name='unique_city_name_en_per_gov'
            ),
            models.UniqueConstraint(
                fields=['governorate', 'name_ar'],
                name='unique_city_name_ar_per_gov'
            ),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.governorate.name_en}-{self.name_en}")
            slug = base
            counter = 1
            while City.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name_en} / {self.name_ar}"
    
    @property
    def name(self):
        from django.utils.translation import get_language
        return self.name_ar if get_language() == 'ar' else self.name_en


class District(models.Model):
    """نموذج الأحياء"""
    
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='districts'
    )
    
    name_en = models.CharField(max_length=100, db_index=True)
    name_ar = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        ordering = ['city__order', 'order', 'name_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['city', 'is_active']),
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
            base = slugify(f"{self.city.governorate.name_en}-{self.city.name_en}-{self.name_en}")
            slug = base
            counter = 1
            while District.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name_en} / {self.name_ar}"
    
    @property
    def name(self):
        from django.utils.translation import get_language
        return self.name_ar if get_language() == 'ar' else self.name_en
    
    @property
    def governorate(self):
        return self.city.governorate
