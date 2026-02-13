# 🌐 دليل القوالب العربية ونظام الترجمة

## 📊 نظرة عامة

تم تصميم المشروع ليكون:
- ✅ **جميع صفحات الموقع بالعربية** (مع دعم RTL كامل)
- ✅ **لوحة Django Admin بالإنجليزية** (فقط)
- ✅ **حقول قاعدة البيانات بالإنجليزية** (كما هي)

---

## 🛠️ البنية الأساسية

### 1. **Middleware للغة**

```python
# apps/core/middleware.py

class AdminEnglishMiddleware:
    """
    يجبر لوحة التحكم على استخدام اللغة الإنجليزية
    جميع الصفحات الأخرى بالعربية
    """
```

**كيف يعمل:**
- لو المسار يبدأ بـ `/admin` → يفعّل اللغة الإنجليزية
- أي مسار آخر → يفعّل اللغة العربية

### 2. **الإعدادات**

```python
# config/settings/base.py

LANGUAGE_CODE = 'ar'  # اللغة الافتراضية

LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',
    'apps.core.middleware.AdminEnglishMiddleware',  # مهم!
    ...
]
```

### 3. **قالب base.html**

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <!-- Bootstrap RTL -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" 
          rel="stylesheet">
    
    <!-- Google Fonts - Cairo -->
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap" 
          rel="stylesheet">
    
    <style>
        body {
            font-family: 'Cairo', sans-serif;
        }
    </style>
</head>
<body>
    <!-- المحتوى هنا -->
</body>
</html>
```

---

## 📝 كيفية كتابة القوالب

### ✅ **ما يجب فعله**

1. **استخدم العربية مباشرة في القوالب:**

```html
<!-- ✅ صحيح -->
<h1>دليل أي خدمة</h1>
<button class="btn btn-primary">إضافة محل</button>
<p>مرحباً بك في دليلنا الشامل</p>
```

2. **استخدم الحقول العربية من الموديل:**

```html
<!-- ✅ صحيح -->
<h2>{{ business.name_ar }}</h2>
<p>{{ business.description_ar }}</p>
<span>{{ category.name_ar }}</span>
```

3. **استخدم Bootstrap RTL:**

```html
<!-- ✅ صحيح -->
<div class="d-flex justify-content-end">
    <button class="btn btn-primary ms-2">حفظ</button>
    <button class="btn btn-secondary">إلغاء</button>
</div>
```

### ❌ **ما يجب تجنبه**

```html
<!-- ❌ خطأ -->
{% load i18n %}
<h1>{% trans 'Business Directory' %}</h1>  <!-- لا حاجة للترجمة -->

<!-- ❌ خطأ -->
<h2>{{ business.name_en }}</h2>  <!-- استخدم name_ar -->

<!-- ❌ خطأ -->
<div class="float-left">  <!-- استخدم float-end في RTL -->
```

---

## 🖌️ أمثلة عملية

### 1. **قائمة المحلات**

```html
<!-- templates/directory/business_list.html -->
{% extends 'base.html' %}

{% block title %}دليل المحلات{% endblock %}

{% block content %}
<div class="container">
    <h1 class="mb-4">دليل المحلات والخدمات</h1>
    
    <div class="row">
        {% for business in businesses %}
        <div class="col-md-4 mb-4">
            <div class="card">
                {% if business.logo %}
                <img src="{{ business.logo.url }}" class="card-img-top" alt="{{ business.name_ar }}">
                {% endif %}
                
                <div class="card-body">
                    <h5 class="card-title">{{ business.name_ar }}</h5>
                    <p class="card-text">{{ business.description_ar|truncatewords:20 }}</p>
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="badge bg-primary">{{ business.category.name_ar }}</span>
                        <a href="{% url 'directory:business_detail' business.slug %}" 
                           class="btn btn-sm btn-outline-primary">
                            مشاهدة التفاصيل
                        </a>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="alert alert-info" role="alert">
                <i class="fas fa-info-circle"></i>
                لا توجد محلات حالياً
            </div>
        </div>
        {% endfor %}
    </div>
    
    <!-- Pagination -->
    {% if businesses.has_other_pages %}
    <nav aria-label="تصفح النتائج">
        <ul class="pagination justify-content-center">
            {% if businesses.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ businesses.previous_page_number }}">السابق</a>
            </li>
            {% endif %}
            
            <li class="page-item active">
                <span class="page-link">صفحة {{ businesses.number }} من {{ businesses.paginator.num_pages }}</span>
            </li>
            
            {% if businesses.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ businesses.next_page_number }}">التالي</a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}
```

### 2. **نموذج إضافة/تعديل**

```html
<!-- templates/directory/business_form.html -->
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}{% if form.instance.pk %}تعديل محل{% else %}إضافة محل جديد{% endif %}{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-store"></i>
                        {% if form.instance.pk %}تعديل بيانات المحل{% else %}إضافة محل جديد{% endif %}
                    </h4>
                </div>
                
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        {{ form|crispy }}
                        
                        <div class="d-flex justify-content-end gap-2 mt-4">
                            <a href="{% url 'directory:business_list' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> إلغاء
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i>
                                {% if form.instance.pk %}تحديث{% else %}إضافة{% endif %}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 3. **الرسائل**

```python
# views.py

from django.contrib import messages

def business_create(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            
            messages.success(request, 'تم إضافة المحل بنجاح!')
            return redirect('directory:business_detail', business.slug)
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    # ...
```

---

## 🎨 أنماط RTL

### **Bootstrap RTL Classes**

| LTR Class | RTL Class | الاستخدام |
|-----------|-----------|----------|
| `ms-2` | `ms-2` | margin-start (يسار في RTL) |
| `me-2` | `me-2` | margin-end (يمين في RTL) |
| `float-start` | `float-start` | يطفو يسار في RTL |
| `float-end` | `float-end` | يطفو يمين في RTL |
| `text-start` | `text-start` | محاذاة يسار في RTL |
| `text-end` | `text-end` | محاذاة يمين في RTL |

**ملاحظة:** Bootstrap 5 RTL يعكس الاتجاهات تلقائياً!

---

## 📦 هيكل الملفات

```
daliil-ay-khidma/
├── templates/
│   ├── base.html                 # القالب الأساسي (عربي)
│   ├── includes/
│   │   ├── navbar.html           # شريط التنقل (عربي)
│   │   └── footer.html           # التذييل (عربي)
│   ├── directory/
│   │   ├── business_list.html
│   │   ├── business_detail.html
│   │   └── business_form.html
│   └── ...
│
├── apps/
│   ├── core/
│   │   └── middleware.py         # Middleware للغة
│   └── ...
│
├── config/
│   └── settings/
│       └── base.py               # الإعدادات
│
└── locale/                       # (اختياري للمستقبل)
    └── ar/
        └── LC_MESSAGES/
            └── django.po
```

---

## ⚙️ التثبيت

### 1. **Pull أحدث التغييرات**

```bash
git pull origin master
```

### 2. **Migrate (إن لزم)**

```bash
python manage.py migrate
```

### 3. **تجميع الملفات الساكنة**

```bash
python manage.py collectstatic --noinput
```

### 4. **إعادة تشغيل السيرفر**

```bash
python manage.py runserver
```

---

## ✅ الفحص والاختبار

### **اختبر اللغة العربية:**

1. افتح `http://127.0.0.1:8000/`
2. تأكد أن الموقع بالعربية وRTL
3. تفقد القوائم، الأزرار، والنصوص

### **اختبر لوحة التحكم:**

1. افتح `http://127.0.0.1:8000/admin/`
2. تأكد أن لوحة التحكم **بالإنجليزية**
3. تفقد القوائم الجانبية والواجهة

---

## 💡 نصائح وممارسات مفضلة

### 1. **التسميات**
- ✅ استخدم `font-family: 'Cairo'` للعربية
- ✅ استخدم `font-weight: 600` أو أعلى للعناوين
- ✅ زد `line-height` ليكون `1.8` أو أكثر

### 2. **المسافات**
- ✅ استخدم `margin-start` بدلاً من `margin-left`
- ✅ استخدم `padding-end` بدلاً من `padding-right`

### 3. **الأيقونات**
- ✅ Font Awesome يدعم RTL تلقائياً
- ✅ استخدم `<i class="fas fa-arrow-left"></i>` للسهم (تنقلب تلقائياً)

### 4. **النماذج (Forms)**
- ✅ استخدم `crispy_forms` مع Bootstrap 5
- ✅ ضع labels بالعربية في الـ Model

```python
class Business(models.Model):
    name_ar = models.CharField('الاسم بالعربية', max_length=200)
    description_ar = models.TextField('الوصف بالعربية')
```

---

## 🔧 الصيانة والتحديث

### **لتحديث قالب موجود:**

1. افتح القالب
2. استبدل النصوص الإنجليزية بالعربية
3. غيّر `business.name_en` إلى `business.name_ar`
4. تأكد من استخدام Bootstrap RTL classes
5. اختبر!

---

## 🐛 حل المشاكل

### **الموقع لسه بالإنجليزية!**
→ تأكد من إضافة `AdminEnglishMiddleware` في `MIDDLEWARE`

### **لوحة التحكم بالعربية!**
→ تأكد من ترتيب `AdminEnglishMiddleware` بعد `LocaleMiddleware`

### **الاتجاه غلط!**
→ تأكد من استخدام `bootstrap.rtl.min.css`
→ تأكد من `<html dir="rtl">`

### **الخط غريب!**
→ تأكد من تحميل Cairo font
→ أضف `font-family: 'Cairo'` في CSS

---

## 🚀 الخطوة القادمة

- [ ] تحديث جميع قوالب `templates/directory/`
- [ ] تحديث جميع قوالب `templates/dashboard/`
- [ ] تحديث `navbar.html` و `footer.html`
- [ ] إضافة validation messages بالعربية
- [ ] إضافة error pages بالعربية (404, 500)

---

## 📞 الدعم

لأي استفسار أو مشكلة، افتح Issue على GitHub أو اتصل بالفريق.

---

**تم بحمد الله! ✨**

*آخر تحديث: {{ تاريخ اليوم }}*
