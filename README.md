# 📍 دليل أي خدمة | Daliil Ay Khidma

## 🎉 نظام دليل خدمات شامل ومتطور 
**Complete Service Directory System**

نظام دليل خدمات متكامل باللغتين العربية والإنجليزية مع كامل الميزات المتقدمة

---

## 🚀 **الميزات الرئيسية | Key Features**

### 🌍 **1. دعم ثنائي اللغة | Bilingual Support**
- ✅ عربي وإنجليزي كامل (Arabic & English)
- ✅ جميع النماذج ثنائية اللغة
- ✅ Automatic language detection
- ✅ SEO-friendly URLs

### 📍 **2. نظام المواقع 3 مستويات | 3-Level Location System**
🏛️ **Governorate** (محافظة)
   └─ 🌆 **City** (مدينة)
       └─ 🏘️ **District** (حي)
           └─ 🏪 **Business** (محل)

### 🏪 **3. إدارة المحلات | Business Management**
- ✅ ملفات كاملة للمحلات
- ✅ صور متعددة (Logo, Cover, Gallery)
- ✅ تفاصيل الاتصال كاملة
- ✅ روابط وسائل التواصل (FB, IG, Twitter, TikTok)
- ✅ Google Maps integration
- ✅ ساعات العمل
- ✅ عدادات مشاهدة ونقرات

### 🛒 **4. نظام المنتجات والخدمات | Products & Services**
- ✅ منتجات وخدمات غير محدودة
- ✅ أسعار وخصومات
- ✅ صور متعددة للمنتجات
- ✅ إدارة المخزون
- ✅ خيارات التوصيل
- ✅ منتجات مميزة

### 🎁 **5. نظام العروض | Deals & Offers System**
- ✅ عروض بالنسبة أو قيمة ثابتة
- ✅ Buy One Get One (BOGO)
- ✅ عروض مجمعة (Bundle Deals)
- ✅ فترات صلاحية محددة
- ✅ حدود استخدام
- ✅ شروط وأحكام
- ✅ تتبع استخدام العروض

### 💳 **6. نظام الاشتراكات | Subscription System**
- ✅ خطط متعددة (Free, Basic, Premium, VIP)
- ✅ ميزات مختلفة لكل خطة
- ✅ أسعار شهرية، ربع سنوية، نصف سنوية، سنوية
- ✅ تجديد تلقائي
- ✅ تتبع المدفوعات
- ✅ إحصائيات متقدمة

### ⭐ **7. نظام التقييمات | Reviews & Ratings**
- ✅ تقييمات 5 نجوم
- ✅ تعليقات ومراجعات
- ✅ موافقة المسؤول على التقييمات

### 🔍 **8. نظام بحث متقدم | Advanced Search**
- ✅ بحث بالاسم
- ✅ بحث بالموقع
- ✅ بحث بالفئة
- ✅ فلترة متقدمة

### 📊 **9. لوحة تحكم متقدمة | Advanced Dashboard**
- ✅ لوحة للمستخدمين
- ✅ لوحة لأصحاب المحلات
- ✅ إحصائيات مفصلة
- ✅ تقارير شاملة

---

## 📦 **البنية التقنية | Tech Stack**

```
🐍 Django 5.x          - Python Web Framework
📦 PostgreSQL/SQLite - Database
🎨 Bootstrap 5        - Frontend Framework
🧊 Crispy Forms       - Beautiful Forms
📷 Pillow             - Image Processing
🌍 i18n               - Internationalization
📧 Django Cleanup     - Auto file cleanup
```

---

## 📁 **هيكل المشروع | Project Structure**

```
daliil-ay-khidma/
├── apps/
│   ├── accounts/          # نظام المستخدمين | Users System
│   ├── core/              # الصفحات الأساسية | Core Pages
│   ├── directory/         # ⭐ نظام الدليل | Directory System
│   │   ├── models/
│   │   │   ├── location.py    # Governorate, City, District
│   │   │   ├── category.py    # Categories
│   │   │   ├── business.py    # Business & BusinessImage
│   │   │   └── favorites.py   # User Favorites
│   │   ├── admin.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── products/          # ✨ نظام المنتجات | Products System (NEW)
│   │   ├── models.py      # Product, ProductImage
│   │   ├── admin.py
│   │   └── ...
│   ├── subscriptions/     # 💳 نظام الاشتراكات | Subscriptions (NEW)
│   │   ├── models.py      # SubscriptionPlan, Subscription
│   │   ├── admin.py
│   │   └── ...
│   ├── deals/             # 🎁 نظام العروض | Deals System (NEW)
│   │   ├── models.py      # Deal, DealClaim
│   │   ├── admin.py
│   │   └── ...
│   ├── categories/        # نظام الفئات | Categories
│   ├── reviews/           # نظام التقييمات | Reviews
│   ├── search/            # نظام البحث | Search
│   ├── dashboard/         # لوحة التحكم | Dashboard
│   └── services/          # الخدمات | Services
├── config/
│   ├── settings/
│   │   ├── base.py        # ✨ Updated with all apps
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
├── static/
├── media/
├── locale/             # ملفات الترجمة | Translation files
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 **التثبيت والتشغيل | Installation & Setup**

### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/sendoo-m/daliil-ay-khidma.git
cd daliil-ay-khidma
```

### 2️⃣ **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Environment Variables**
Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5️⃣ **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ **Create Superuser**
```bash
python manage.py createsuperuser
```

### 7️⃣ **Compile Translations** (اختياري)
```bash
python manage.py compilemessages
```

### 8️⃣ **Run Development Server**
```bash
python manage.py runserver
```

🎉 **Open:** http://127.0.0.1:8000/

---

## 📚 **نماذج البيانات | Database Models**

### **Directory App**
- `Governorate` - محافظة
- `City` - مدينة
- `District` - حي
- `Category` - فئة
- `Business` - محل تجاري
- `BusinessImage` - صور المحل
- `Favorite` - المفضلة

### **Products App** ✨
- `Product` - منتج/خدمة
- `ProductImage` - صور المنتج

### **Subscriptions App** 💳
- `SubscriptionPlan` - خطة اشتراك
- `Subscription` - اشتراك

### **Deals App** 🎁
- `Deal` - عرض
- `DealClaim` - استخدام عرض

### **Reviews App**
- `Review` - تقييم

---

## 🔧 **المتطلبات | Requirements**

```txt
Django>=5.0
Pillow>=10.0
django-crispy-forms
crispy-bootstrap5
django-cleanup
python-decouple
psycopg2-binary  # for PostgreSQL
```

---

## 🛡️ **الأمان | Security Features**

- ✅ CSRF Protection
- ✅ SQL Injection Prevention
- ✅ XSS Protection
- ✅ Password Validation
- ✅ Secure File Upload
- ✅ Environment Variables

---

## 📝 **الرخصة | License**

MIT License

---

## 👨‍💻 **المطور | Developer**

**Sendoo M.**
- GitHub: [@sendoo-m](https://github.com/sendoo-m)

---

## ✨ **التحديثات الأخيرة | Recent Updates**

### v2.0.0 (January 2026) 🎉
- ✨ Added complete Products & Services system
- 💳 Added advanced Subscription system with multiple plans
- 🎁 Added Deals & Offers system with claims tracking
- 🌍 Enhanced bilingual support across all models
- 📊 Improved admin interface with statistics
- 🔒 Enhanced security features

---

## 🚀 **الخطط المستقبلية | Future Plans**

- [ ] REST API (Django REST Framework)
- [ ] Mobile App (Flutter)
- [ ] Payment Gateway Integration
- [ ] Advanced Analytics Dashboard
- [ ] Email Notifications
- [ ] SMS Integration
- [ ] Social Media Login
- [ ] Advanced Reporting System

---

💬 **للاستفسار والدعم | For Support & Questions**

Open an issue on [GitHub](https://github.com/sendoo-m/daliil-ay-khidma/issues)

---

**Made with ❤️ in Egypt**
