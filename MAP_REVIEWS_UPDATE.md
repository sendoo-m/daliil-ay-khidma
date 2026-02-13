# 📍 **تحديث: الخريطة ونظام التقييمات**

## ✅ **ما تم إصلاحه**

### 1️⃣ **موقع الخريطة - تم نقلها!**

#### ✅ **الآن:**
```
الخريطة موجودة في السايدبار أسفل معلومات الاتصال

الترتيب:
1. أزرار الاتصال السريعة
2. معلومات الاتصال
3. 🗺️ الخريطة التفاعلية ⭐
```

---

### 2️⃣ **نظام التقييمات الكامل**

#### ✅ **المميزات:**

```
⭐ عرض جميع التقييمات
⭐ متوسط التقييم مع عدد النجوم
⭐ زر "أضف تقييمك" للمستخدمين المسجلين
⭐ Modal تفاعلي لإضافة تقييم
⭐ نظام نجوم تفاعلي (1-5 نجمة)
⭐ حقل تعليق اختياري
```

---

## 🏪 **للمحلات والحرف** (`business_detail.html`)

### 🗺️ **الخريطة:**
- **الموقع:** في السايدبار أسفل معلومات الاتصال
- **الارتفاع:** 350px
- **الأيقونة:** 📍 بنفسجي
- **زر الاتجاهات:** يفتح Google Maps

### ⭐ **التقييمات:**
- **في Tab مستقل** مع المنتجات
- عرض متوسط التقييم في الأعلى
- زر "أضف تقييمك" في الأعلى
- قائمة بجميع التقييمات

---

## 🏛️ **للخدمات العامة** (`service_detail.html`)

### 🗺️ **الخريطة:**
- **الموقع:** في السايدبار أسفل معلومات الاتصال
- **الارتفاع:** 400px (أكبر)
- **الأيقونة:** 🏛️ سيان
- **زر الاتجاهات:** كبير وبارز

### ⭐ **التقييمات:**
- **في قسم مستقل** بتصميم مميز
- عرض متوسط التقييم بارز
- زر "أضف تقييم" في الأعلى
- قائمة بجميع التقييمات

---

## 🛠️ **التقنيات المستخدمة**

### 🗺️ **الخريطة:**
```javascript
// Leaflet.js v1.9.4
// OpenStreetMap Tiles
// Custom Marker Icons
// Interactive Popups
// Responsive Design
```

### ⭐ **التقييمات:**
```html
<!-- Bootstrap 5 Modal -->
<!-- FontAwesome Stars -->
<!-- Interactive Star Rating -->
<!-- Django Form Processing -->
```

---

## 💻 **متطلبات العمل**

### 1️⃣ **للخرائط:**
```python
# تأكد من وجود الحقول في Model
class Business(models.Model):
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
```

### 2️⃣ **للتقييمات:**

#### **أ. URL Pattern:**
```python
# urls.py
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<slug:business_slug>/', views.add_review, name='add_review'),
]
```

#### **ب. View:**
```python
# views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Business, Review

@login_required
def add_review(request, business_slug):
    if request.method == 'POST':
        business = get_object_or_404(Business, slug=business_slug)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        # تحقق إذا كان المستخدم قيّم مسبقًا
        existing_review = Review.objects.filter(
            business=business, 
            user=request.user
        ).first()
        
        if existing_review:
            # تحديث التقييم القديم
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
            messages.success(request, 'تم تحديث تقييمك بنجاح!')
        else:
            # إضافة تقييم جديد
            Review.objects.create(
                business=business,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'شكرًا لتقييمك!')
        
        return redirect('directory:business_detail', slug=business_slug)
    
    return redirect('directory:home')
```

#### **ج. Model:**
```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    business = models.ForeignKey(
        Business, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='التقييم'
    )
    comment = models.TextField(
        blank=True, 
        null=True,
        verbose_name='التعليق'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإضافة'
    )
    
    class Meta:
        unique_together = ['business', 'user']
        ordering = ['-created_at']
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقييمات'
    
    def __str__(self):
        return f'{self.user.username} - {self.business.name_ar} ({self.rating}⭐)'
```

#### **د. Business Model Methods:**
```python
# في Business Model
from django.db.models import Avg

class Business(models.Model):
    # ... باقي الحقول
    
    def get_average_rating(self):
        """ حساب متوسط التقييم """
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0
    
    def get_total_reviews(self):
        """ عدد التقييمات الكلي """
        return self.reviews.count()
```

#### **هـ. View Context:**
```python
# في business_detail view
def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    
    context = {
        'business': business,
        'products': business.products.all(),
        'reviews': business.reviews.all()[:10],  # أحدث 10 تقييمات
        'average_rating': business.get_average_rating(),
        'total_reviews': business.get_total_reviews(),
    }
    
    # اختيار القالب
    if business.business_type == 'public_service':
        template = 'directory/service_detail.html'
    else:
        template = 'directory/business_detail.html'
    
    return render(request, template, context)
```

---

## 🚀 **خطوات التفعيل**

### **1. Pull التحديثات:**
```bash
git pull origin master
```

### **2. إضافة Review Model:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **3. إضافة URLs:**
```python
# في urls.py الرئيسي
from django.urls import path, include

urlpatterns = [
    # ...
    path('reviews/', include('reviews.urls')),
]
```

### **4. تشغيل السيرفر:**
```bash
python manage.py runserver 0.0.0.0:8008
```

---

## 🎉 **النتيجة النهائية**

### ✅ **للمحلات:**
```
[المحتوى الرئيسي]            [السايدبار]
- وصف المحل                - أزرار اتصال
- منتجات                      - معلومات اتصال
- تقييمات بزر إضافة     - 🗺️ خريطة 350px
```

### ✅ **للخدمات العامة:**
```
[المحتوى الرئيسي]            [السايدبار]
- وصف الخدمة              - أزرار اتصال
- تقييمات بزر إضافة     - معلومات اتصال
                                - 🗺️ خريطة 400px
```

---

✨ **مبروك! الخريطة والتقييمات تعمل بشكل مثالي!** 🗺️⭐
