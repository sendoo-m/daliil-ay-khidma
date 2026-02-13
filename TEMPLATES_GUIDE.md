# 📚 **دليل قوالب دليل أي خدمة**

## 🏪 **صفحة تفاصيل المحلات** (`business_detail.html`)

### متى تستخدمها؟
تستخدم لعرض **المحلات التجارية** التي:
- ✅ لديها **منتجات** للبيع
- ✅ لديها **أسعار**
- ✅ لديها **عروض وخصومات**
- ✅ لديها **معرض صور**

### أمثلة:
```
- محل ملابس 👕
- مطعم 🍕
- مقهى ☕
- سوبر ماركت 🛍️
- محل إلكترونيات 📱
- صيدلية 💊
```

### الميزات:
- 📦 **عرض المنتجات** مع الأسعار
- 🏷️ **بطاقات الخصومات**
- 🖼️ **معرض صور المحل**
- ⭐ **نظام التقييمات**
- 📍 **خريطة تفاعلية**
- 📞 **أزرار الاتصال والواتساب**
- 📊 **إحصائيات مفصلة**

---

## ⚙️ **صفحة تفاصيل الخدمات** (`service_detail.html`)

### متوى تستخدمها؟
تستخدم لعرض **الخدمات العامة** التي:
- ❌ **ليس لديها منتجات** للبيع
- ✅ تقدم **خدمات فقط**
- ✅ معلومات اتصال مفصلة
- ✅ **خريطة بارزة** للوصول

### أمثلة:
```
- عيادة طبية 🏥
- مركز صيانة 🔧
- مكتب محاماة ⚖️
- مكتب محاسبة 📊
- مركز تعليمي 🏫
- صالون حلاقة ✂️
- جيم رياضي 🏋️
```

### الميزات:
- 📍 **خريطة كبيرة** مع زر "احصل على الاتجاهات"
- 📞 **معلومات اتصال بارزة**
- ⭐ **نظام التقييمات** (موجود)
- 📄 **وصف مفصّل للخدمة**
- 📊 **إحصائيات بسيطة**
- ❌ **بدون عرض منتجات**

---

## 🔄 **كيفية الاستخدام في Django View**

### **في `views.py`:**

```python
from django.shortcuts import render, get_object_or_404
from .models import Business

def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    
    # تحديد القالب بناءً على نوع العمل
    if business.business_type == 'service':  # خدمة عامة
        template = 'directory/service_detail.html'
    else:  # محل تجاري
        template = 'directory/business_detail.html'
    
    context = {
        'business': business,
        # ... باقي البيانات
    }
    
    return render(request, template, context)
```

### **أو استخدم فئة العمل:**

```python
def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    
    # إذا كانت الفئة من فئات الخدمات
    service_categories = ['health', 'legal', 'education', 'fitness']
    
    if business.category.slug in service_categories:
        template = 'directory/service_detail.html'
    else:
        template = 'directory/business_detail.html'
    
    context = {'business': business}
    return render(request, template, context)
```

---

## 🎨 **الفروقات التصميمية**

| الميزة | محل تجاري | خدمة عامة |
|---------|------------|-------------|
| **اللون الأساسي** | 🔵 أزرق/بنفسجي | 🔵 أزرق/بنفسجي |
| **عرض المنتجات** | ✅ نعم | ❌ لا |
| **الخريطة** | ✅ في السايدبار | ✅ **بارزة في الوسط** |
| **معرض الصور** | ✅ نعم | ❌ لا |
| **التقييمات** | ✅ نعم | ✅ نعم |
| **زر الاتجاهات** | ✅ في الخريطة | ✅ **زر كبير** |
| **التركيز** | على المنتجات | على التواصل |

---

## 📝 **ملاحظات مهمة**

### 1️⃣ **إضافة حقل في Model:**

```python
class Business(models.Model):
    # ... باقي الحقول
    business_type = models.CharField(
        max_length=20,
        choices=[
            ('shop', 'محل تجاري'),
            ('service', 'خدمة عامة')
        ],
        default='shop'
    )
```

### 2️⃣ **تفعيل الخريطة:**
- ✅ تأكد من وجود `latitude` و `longitude` في البيانات
- ✅ الخريطة تستخدم **Leaflet.js** مع **OpenStreetMap**
- ✅ زر الاتجاهات يفتح **Google Maps**

### 3️⃣ **التقييمات:**
- ✅ موجودة في **كلا الصفحتين**
- ✅ نفس النظام والتصميم

---

## 🚀 **للتفعيل:**

```bash
# 1. Pull التحديثات
git pull origin master

# 2. تطبيق التغييرات على القاعدة
python manage.py makemigrations
python manage.py migrate

# 3. تجميع Static Files
python manage.py collectstatic --noinput

# 4. تشغيل السيرفر
python manage.py runserver 0.0.0.0:8008
```

---

## 🎯 **مثال عملي**

### **محل ملابس (يستخدم business_detail.html):**
```
URL: /business/fashion-store/
يعرض:
- منتجات بأسعارها 👔
- خصومات وعروض 🏷️
- معرض صور 🖼️
- خريطة في السايدبار 📍
```

### **عيادة طبية (يستخدم service_detail.html):**
```
URL: /service/health-clinic/
يعرض:
- وصف مفصّل للخدمة 🏥
- خريطة كبيرة بارزة 🗺️
- زر احصل على الاتجاهات 🧭
- معلومات اتصال بارزة 📞
- بدون منتجات ❌
```

---

✨ **مبروك! لديك الآن صفحتين مختلفتين لتجربة مستخدم أفضل!** 🎉
