# 📚 **دليل قوالب دليل أي خدمة**

## 📌 **نظرة عامة**

الموقع يحتوي على **3 أنواع** من الكيانات:

### 1️⃣ **محلات تجارية** 🏪
- محلات ملابس
- مطاعم
- مقاهي
- سوبر ماركت
- صيدليات

### 2️⃣ **خدمات وحرف (أشخاص)** 🔧
- نجار
- سباك
- كهربائي
- حداد
- بلاط
- مقاول بناء

### 3️⃣ **خدمات عامة (غير مملوكة)** 🏛️
- مستشفيات حكومية
- حدائق عامة
- مساجد
- كنائس
- مواقف عامة
- محطات قطار
- مكاتب حكومية

---

## 🏪 **صفحة تفاصيل المحلات** (`business_detail.html`)

### 🎯 **متى تستخدمها؟**
تستخدم لعرض:
- ✅ **المحلات التجارية** (مطاعم، محلات)
- ✅ **الحرف والخدمات الشخصية** (نجار، سباك، كهربائي)

### 🎨 **الميزات:**

#### ✅ **عرض المنتجات/الخدمات**
```
- بطاقات منتجات بالأسعار
- عرض الخصومات
- صور المنتجات
- Tabs للتنقل بين المنتجات والتقييمات
```

#### 🗺️ **خريطة تفاعلية**
```
- موجودة في المحتوى الرئيسي
- ارتفاع 450px
- زر "احصل على الاتجاهات"
- Popup عند الضغط على العلامة
```

#### ⭐ **نظام التقييمات**
```
- عرض جميع التقييمات
- إضافة تقييم جديد
- متوسط التقييم
```

#### 📊 **إحصائيات**
```
- عدد المشاهدات
- متوسط التقييم
- عدد المنتجات
- عدد التقييمات
```

#### 📞 **أزرار الاتصال**
```
- زر اتصال هاتفي
- زر واتساب
- زر إضافة للمفضلة
```

### 🎨 **الألوان:**
- **Primary:** `#667eea` (أزرق/بنفسجي)
- **Gradient:** `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`

---

## 🏛️ **صفحة تفاصيل الخدمات العامة** (`service_detail.html`)

### 🎯 **متى تستخدمها؟**
تستخدم لعرض **الخدمات العامة غير المملوكة** فقط:
- ✅ مستشفيات حكومية
- ✅ حدائق عامة
- ✅ مساجد وكنائس
- ✅ مواقف عامة
- ✅ محطات قطار/مترو
- ✅ مكاتب حكومية

### 🎨 **الميزات:**

#### 🗺️ **خريطة كبيرة بارزة**
```
- ارتفاع 500px (أكبر من المحلات)
- في الوسط البارز
- زر اتجاهات كبير ومميّز
- تركيز على سهولة الوصول
```

#### ❌ **بدون منتجات**
```
- لا يوجد Tabs للمنتجات
- لا يوجد عرض أسعار
- التركيز على المعلومات
```

#### ⭐ **نظام التقييمات**
```
- موجود ويعمل بشكل كامل
- نفس التصميم كالمحلات
- يمكن للمستخدمين تقييم الخدمة
```

#### 📞 **معلومات اتصال مفصّلة**
```
- بطاقات معلومات أكبر
- تصميم بارز للعنوان
- ساعات العمل
```

#### 📊 **إحصائيات بسيطة**
```
- عدد المشاهدات
- متوسط التقييم
- عدد المراجعات
(بدون عدد المنتجات)
```

### 🎨 **الألوان:**
- **Primary:** `#06b6d4` (سيان/سماوي)
- **Gradient:** `linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)`

---

## 🔄 **مقارنة سريعة**

| الميزة | محلات + حرف | خدمات عامة |
|---------|---------------|----------------|
| **القالب** | `business_detail.html` | `service_detail.html` |
| **اللون** | 🔵 أزرق/بنفسجي | 🔵 سيان/سماوي |
| **المنتجات** | ✅ نعم | ❌ لا |
| **الخريطة** | ✅ 450px | ✅ **500px** |
| **موقع الخريطة** | في المحتوى | **بارزة في الوسط** |
| **التقييمات** | ✅ نعم | ✅ نعم |
| **الأسعار** | ✅ نعم | ❌ لا |
| **التركيز** | على المنتجات | على الوصول |

---

## 💻 **كيفية الاستخدام في Django**

### **الطريقة الأولى: حسب نوع العمل**

```python
# في views.py
from django.shortcuts import render, get_object_or_404
from .models import Business

def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    
    # تحديد القالب بناءً على النوع
    if business.business_type == 'public_service':
        template = 'directory/service_detail.html'
    else:
        # محلات تجارية أو حرف
        template = 'directory/business_detail.html'
    
    context = {
        'business': business,
        'products': business.products.all(),
        'reviews': business.reviews.all()[:5],
        'average_rating': business.get_average_rating(),
        'total_reviews': business.reviews.count(),
    }
    
    return render(request, template, context)
```

### **الطريقة الثانية: حسب الفئة**

```python
def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    
    # فئات الخدمات العامة
    PUBLIC_SERVICE_CATEGORIES = [
        'hospital-gov',     # مستشفى حكومي
        'park',             # حديقة
        'mosque',           # مسجد
        'church',           # كنيسة
        'parking',          # موقف
        'train-station',    # محطة قطار
        'metro-station',    # محطة مترو
        'gov-office',       # مكتب حكومي
    ]
    
    if business.category.slug in PUBLIC_SERVICE_CATEGORIES:
        template = 'directory/service_detail.html'
    else:
        template = 'directory/business_detail.html'
    
    context = {'business': business}
    return render(request, template, context)
```

---

## 📦 **متطلبات Model**

### **أضف هذا الحقل للتفريق:**

```python
# models.py
class Business(models.Model):
    BUSINESS_TYPES = [
        ('shop', 'محل تجاري'),
        ('craft', 'حرفة/خدمة شخصية'),
        ('public_service', 'خدمة عامة'),
    ]
    
    business_type = models.CharField(
        max_length=20,
        choices=BUSINESS_TYPES,
        default='shop',
        verbose_name='نوع العمل'
    )
    
    # للخريطة
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='خط العرض'
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='خط الطول'
    )
```

---

## 🗺️ **مشكلة عدم ظهور الخريطة - تم إصلاحها! ✅**

### **المشكلة:**
كان هناك خطأ في URL خرائط OpenStreetMap

### **الحل:**
```javascript
// ✅ الصحيح
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© أوبن ستريت ماب',
    maxZoom: 19
}).addTo(map);

// ❌ الخطأ القديم
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}/png', ...)
//                                                             ^^^^ الخطأ هنا
```

---

## 🎉 **أمثلة عملية**

### **1️⃣ محل ملابس** 👔
```
URL: /business/fashion-store/
القالب: business_detail.html

يعرض:
✅ منتجات بالأسعار
✅ عروض وخصومات
✅ خريطة 450px
✅ تقييمات
```

### **2️⃣ نجار** 🔨
```
URL: /business/carpenter-ali/
القالب: business_detail.html

يعرض:
✅ خدمات بالأسعار
✅ معرض أعمال
✅ خريطة 450px
✅ تقييمات
```

### **3️⃣ مستشفى حكومي** 🏭
```
URL: /service/public-hospital/
القالب: service_detail.html

يعرض:
❌ بدون منتجات
✅ خريطة 500px بارزة
✅ زر اتجاهات كبير
✅ معلومات اتصال مفصّلة
✅ تقييمات
```

---

## 🚀 **للتفعيل:**

```bash
# 1. Pull التحديثات
git pull origin master

# 2. إضافة حقل business_type
python manage.py makemigrations
python manage.py migrate

# 3. تجميع Static Files
python manage.py collectstatic --noinput

# 4. تشغيل
python manage.py runserver 0.0.0.0:8008
```

---

## ✅ **ما تم إصلاحه:**

1. ✅ **مشكلة عدم ظهور الخريطة** - تم إصلاح URL
2. ✅ **خريطة تفاعلية** للمحلات والحرف
3. ✅ **خريطة بارزة كبيرة** للخدمات العامة
4. ✅ **زر اتجاهات Google Maps** لسهولة الوصول
5. ✅ **Popup تفاعلي** عند الضغط على العلامة

---

✨ **مبروك! الخرائط تعمل الآن بشكل مثالي!** 🎉🗺️
