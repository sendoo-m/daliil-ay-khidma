# 📍 دليل أي خدمة | Daliil Ay Khidma

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Made in Egypt](https://img.shields.io/badge/Made%20in-Egypt%20🇪🇬-red.svg)](https://github.com/sendoo-m)

**نظام دليل خدمات متكامل وشامل | Comprehensive Service Directory System**

منصة متطورة لإدارة دليل الخدمات والمحلات التجارية بميزات احترافية ودعم كامل للغتين العربية والإنجليزية

*An advanced platform for managing service directories and businesses with professional features and full bilingual support*

[العربية](#arabic) • [English](#english) • [التثبيت](#installation) • [التوثيق](#documentation)

</div>

---

## 🎯 نظرة عامة | Overview

**دليل أي خدمة** هو نظام متكامل مبني بإطار Django لإدارة دليل الخدمات والمحلات التجارية. يوفر النظام حلاً شاملاً لعرض وإدارة الأعمال التجارية مع دعم كامل للغتين العربية والإنجليزية، ونظام موقع جغرافي متقدم، وميزات تسويقية قوية.

**Daliil Ay Khidma** is a comprehensive Django-based service directory management system. It provides a complete solution for displaying and managing businesses with full bilingual support (Arabic & English), advanced geographic location system, and powerful marketing features.

---

## ✨ الميزات الرئيسية | Key Features

### 🌍 دعم ثنائي اللغة | Bilingual Support
- ✅ **واجهة كاملة بالعربية والإنجليزية** | Complete Arabic and English interface
- ✅ **جميع النماذج ثنائية اللغة** | All models are bilingual
- ✅ **اكتشاف تلقائي للغة** | Automatic language detection
- ✅ **روابط صديقة لمحركات البحث (SEO)** | SEO-friendly URLs
- ✅ **ترجمة ديناميكية للمحتوى** | Dynamic content translation

### 📍 نظام المواقع الجغرافية (3 مستويات) | Location System (3 Levels)
```
🏛️ محافظة | Governorate
   └─ 🌆 مدينة | City
       └─ 🏘️ حي | District
           └─ 🏪 محل تجاري | Business
```
- تصنيف جغرافي دقيق ومنظم
- بحث متقدم بالموقع
- خرائط تفاعلية
- تكامل مع Google Maps

### 🏪 إدارة المحلات التجارية | Business Management
- ✅ **ملفات تعريفية شاملة** | Comprehensive business profiles
- ✅ **صور متعددة** (لوجو، غلاف، معرض صور) | Multiple images (logo, cover, gallery)
- ✅ **تفاصيل اتصال كاملة** | Complete contact details
- ✅ **روابط وسائل التواصل** (Facebook, Instagram, Twitter, TikTok) | Social media links
- ✅ **تكامل خرائط جوجل** | Google Maps integration
- ✅ **ساعات العمل** | Working hours
- ✅ **عدادات مشاهدة ونقرات** | View and click counters
- ✅ **أنواع متعددة من الأعمال** (متجر فعلي، متجر إلكتروني، خدمة، مختلط) | Multiple business types

### 🛒 نظام المنتجات والخدمات | Products & Services System
- ✅ **منتجات وخدمات غير محدودة** | Unlimited products and services
- ✅ **نظام تسعير مرن** (سعر أساسي، سعر مخفض) | Flexible pricing (base price, discounted price)
- ✅ **معرض صور للمنتجات** | Product image gallery
- ✅ **إدارة المخزون المتقدمة** | Advanced inventory management
- ✅ **خيارات توصيل متنوعة** | Various delivery options
- ✅ **منتجات مميزة** | Featured products
- ✅ **تصنيف حسب النوع** (منتج، خدمة) | Classification by type

### 🎁 نظام العروض والخصومات | Deals & Offers System
- ✅ **أنواع عروض متعددة:**
  - 💯 **خصم بالنسبة المئوية** | Percentage discount
  - 💵 **خصم بقيمة ثابتة** | Fixed amount discount
  - 🎉 **اشترِ واحد واحصل على آخر** (BOGO) | Buy One Get One
  - 📦 **عروض حزم المنتجات** | Bundle deals
- ✅ **فترات صلاحية محددة** | Specific validity periods
- ✅ **حدود استخدام للعروض** | Usage limits for offers
- ✅ **شروط وأحكام مخصصة** | Custom terms and conditions
- ✅ **تتبع دقيق لاستخدام العروض** | Accurate deal usage tracking

### 💳 نظام الاشتراكات | Subscription System
- ✅ **خطط متعددة:** Free | Basic | Premium | VIP
- ✅ **ميزات مميزة لكل خطة** | Unique features for each plan
- ✅ **فترات اشتراك مرنة:**
  - شهري | Monthly
  - ربع سنوي | Quarterly
  - نصف سنوي | Semi-annual
  - سنوي | Annual
- ✅ **تجديد تلقائي** | Auto-renewal
- ✅ **تتبع المدفوعات** | Payment tracking
- ✅ **إحصائيات متقدمة لكل خطة** | Advanced plan statistics

### ⭐ نظام التقييمات والمراجعات | Reviews & Ratings System
- ✅ **تقييم بنظام 5 نجوم** | 5-star rating system
- ✅ **تعليقات ومراجعات مفصلة** | Detailed comments and reviews
- ✅ **نظام موافقة المسؤول** | Admin approval system
- ✅ **ردود أصحاب الأعمال** | Business owner replies
- ✅ **حساب متوسط التقييمات** | Average rating calculation

### 🔍 نظام بحث متقدم | Advanced Search System
- ✅ **بحث بالاسم** | Search by name
- ✅ **بحث بالموقع الجغرافي** | Search by location
- ✅ **بحث بالفئة** | Search by category
- ✅ **فلاتر متقدمة** | Advanced filters
- ✅ **بحث بالقرب من موقعك** | Nearby search
- ✅ **ترتيب النتائج** (حسب التقييم، المشاهدات، التاريخ) | Result ordering

### 📊 لوحات تحكم احترافية | Professional Dashboards

#### 👤 لوحة المستخدمين | User Dashboard
- إحصائيات شخصية
- المفضلة المحفوظة
- التقييمات المقدمة
- سجل النشاطات

#### 🏢 لوحة أصحاب الأعمال | Business Owner Dashboard
- 📈 **رسوم بيانية تفاعلية** (Chart.js)
- 📊 **إحصائيات شاملة** (مشاهدات، نقرات، تقييمات)
- 🎯 **مؤشرات أداء رئيسية (KPIs)**
- 📉 **تتبع الأداء الشهري**
- 🏆 **ترتيب الأعمال حسب الأداء**
- ⚡ **إجراءات سريعة** لإدارة المحتوى
- 🔔 **سجل النشاطات الأخيرة**

---

## 📦 البنية التقنية | Tech Stack

### Backend
```yaml
Framework: Django 5.0+
Language: Python 3.11+
Database: PostgreSQL / SQLite
API: Django REST Framework
Authentication: JWT (Simple JWT)
```

### Frontend
```yaml
UI Framework: Bootstrap 5.3
Icons: Font Awesome 6.x
Charts: Chart.js 4.4.0
Forms: Django Crispy Forms + Crispy Bootstrap 5
```

### Additional Libraries
```yaml
Images: Pillow + django-imagekit
Internationalization: django-modeltranslation
API Documentation: drf-spectacular
CORS: django-cors-headers
Testing: pytest + pytest-django
```

---

## 📁 هيكل المشروع | Project Structure

```
daliil-ay-khidma/
├── 📂 apps/
│   ├── 👥 accounts/         # نظام المستخدمين والصلاحيات | Users & Permissions
│   ├── 🎨 core/             # الصفحات الأساسية | Core Pages  
│   ├── 📍 directory/        # نظام الدليل الرئيسي | Main Directory
│   │   ├── models/
│   │   │   ├── location.py   # المواقع الجغرافية | Locations
│   │   │   ├── category.py   # التصنيفات | Categories
│   │   │   ├── business.py   # الأعمال التجارية | Businesses
│   │   │   └── favorites.py  # المفضلة | Favorites
│   │   ├── admin.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── 🛍️ products/         # المنتجات والخدمات | Products & Services
│   ├── 💳 subscriptions/    # الاشتراكات | Subscriptions
│   ├── 🎁 deals/            # العروض والخصومات | Deals & Offers
│   ├── 🏷️ categories/       # إدارة الفئات | Categories Management
│   ├── ⭐ reviews/          # التقييمات | Reviews
│   ├── 🔍 search/           # البحث المتقدم | Advanced Search
│   ├── 📊 dashboard/        # لوحات التحكم | Dashboards
│   ├── 🔧 services/         # الخدمات المساعدة | Helper Services
│   └── 🌐 api/              # REST API
├── ⚙️ config/
│   ├── settings/
│   │   ├── base.py          # إعدادات أساسية | Base settings
│   │   ├── development.py   # بيئة التطوير | Development
│   │   └── production.py    # بيئة الإنتاج | Production
│   ├── urls.py
│   └── wsgi.py
├── 🎨 templates/            # قوالب HTML | HTML Templates
├── 📦 static/               # ملفات ثابتة | Static Files
├── 📸 media/                # ملفات المستخدمين | User Uploads
├── 🌍 locale/               # ملفات الترجمة | Translation Files
├── 🔧 fixtures/             # بيانات أولية | Initial Data
├── 📝 logs/                 # سجلات النظام | System Logs
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 التثبيت والتشغيل | Installation & Setup

### المتطلبات الأساسية | Prerequisites
- Python 3.11 أو أحدث | Python 3.11 or higher
- PostgreSQL 14+ (اختياري، SQLite متاح) | PostgreSQL 14+ (optional, SQLite available)
- Git

### 1️⃣ استنساخ المستودع | Clone Repository
```bash
git clone https://github.com/sendoo-m/daliil-ay-khidma.git
cd daliil-ay-khidma
```

### 2️⃣ إنشاء بيئة افتراضية | Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ تثبيت المكتبات | Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ إعداد ملف المتغيرات البيئية | Setup Environment Variables
قم بإنشاء ملف `.env` في المجلد الرئيسي:
```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite default)
DATABASE_URL=sqlite:///db.sqlite3

# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/daliil_db

# Language
LANGUAGE_CODE=ar
TIME_ZONE=Africa/Cairo

# Media & Static
MEDIA_URL=/media/
STATIC_URL=/static/
```

### 5️⃣ تطبيق الترحيلات | Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ إنشاء مستخدم مسؤول | Create Superuser
```bash
python manage.py createsuperuser
```

### 7️⃣ تحميل البيانات الأولية (اختياري) | Load Initial Data (Optional)
```bash
python manage.py loaddata fixtures/governorates.json
python manage.py loaddata fixtures/categories.json
```

### 8️⃣ ترجمة النصوص (اختياري) | Compile Translations (Optional)
```bash
python manage.py compilemessages
```

### 9️⃣ جمع الملفات الثابتة (للإنتاج) | Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### 🔟 تشغيل الخادم | Run Development Server
```bash
python manage.py runserver
```

🎉 **افتح المتصفح على:** | **Open browser at:** 
http://127.0.0.1:8000/

---

## 📚 نماذج البيانات | Database Models

### Directory App - تطبيق الدليل
| Model | Description AR | Description EN |
|-------|---------------|----------------|
| `Governorate` | المحافظات | Governorates |
| `City` | المدن | Cities |
| `District` | الأحياء | Districts |
| `Category` | الفئات والتصنيفات | Categories |
| `Business` | المحلات التجارية | Businesses |
| `BusinessImage` | صور المحلات | Business Images |
| `Favorite` | المفضلة | Favorites |

### Products App - تطبيق المنتجات
| Model | Description |
|-------|-------------|
| `Product` | المنتجات والخدمات |
| `ProductImage` | صور المنتجات |

### Subscriptions App - تطبيق الاشتراكات
| Model | Description |
|-------|-------------|
| `SubscriptionPlan` | خطط الاشتراك |
| `Subscription` | اشتراكات المستخدمين |

### Deals App - تطبيق العروض
| Model | Description |
|-------|-------------|
| `Deal` | العروض والخصومات |
| `DealClaim` | سجل استخدام العروض |

### Reviews App - تطبيق التقييمات
| Model | Description |
|-------|-------------|
| `Review` | التقييمات والمراجعات |

---

## 🔒 ميزات الأمان | Security Features

- ✅ **حماية CSRF** | CSRF Protection
- ✅ **منع حقن SQL** | SQL Injection Prevention  
- ✅ **حماية XSS** | XSS Protection
- ✅ **تحقق قوي من كلمات المرور** | Strong password validation
- ✅ **رفع آمن للملفات** | Secure file upload
- ✅ **متغيرات بيئية محمية** | Protected environment variables
- ✅ **HTTPS في الإنتاج** | HTTPS in production
- ✅ **مصادقة JWT للـ API** | JWT Authentication for API

---

## 📖 التوثيق | Documentation

- 📘 [توثيق API الكامل](API_DOCUMENTATION.md) | [Complete API Documentation](API_DOCUMENTATION.md)
- 📗 [تحسينات لوحة التحكم](DASHBOARD_UPGRADE.md) | [Dashboard Enhancements](DASHBOARD_UPGRADE.md)
- 📕 [سجل التغييرات](CHANGELOG.md) | [Changelog](CHANGELOG.md)
- 📙 [ملخص إصلاحات الأخطاء](BUGFIX_SUMMARY.md) | [Bug Fixes Summary](BUGFIX_SUMMARY.md)

---

## 🛡️ الاختبارات | Testing

```bash
# تشغيل جميع الاختبارات | Run all tests
pytest

# تشغيل اختبارات محددة | Run specific tests
pytest apps/directory/tests/

# مع تغطية الكود | With code coverage
pytest --cov=apps --cov-report=html

# تشغيل اختبارات سريعة | Run quick tests
pytest -x --ff
```

---

## 🌐 REST API

النظام يوفر REST API شامل يدعم:
- 🔑 مصادقة JWT
- 📱 API عام للتطبيقات
- 🏢 API لأصحاب الأعمال
- 👨‍💼 API للمسؤولين

**الوصول للتوثيق:**
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`
- JSON Schema: `http://localhost:8000/api/schema/`

[📖 اطلع على التوثيق الكامل](API_DOCUMENTATION.md)

---

## 🚀 النشر | Deployment

### استخدام Gunicorn
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### استخدام Docker
```bash
# بناء الصورة | Build image
docker build -t daliil-ay-khidma .

# تشغيل الحاوية | Run container
docker run -p 8000:8000 daliil-ay-khidma
```

### استخدام Docker Compose
```bash
docker-compose up -d
```

---

## 📊 الإصدارات | Versions

### v2.1.1 (الحالي) | v2.1.1 (Current)
- ✅ إصلاح جميع الأخطاء المعروفة
- ✅ تحسين الأداء
- ✅ تحديث لوحة التحكم

### v2.1.0 (فبراير 2026)
- ✨ لوحة تحكم محسّنة مع رسوم بيانية
- 📊 إحصائيات متقدمة
- 🎨 تصميم عصري

### v2.0.0 (يناير 2026)
- ✨ نظام المنتجات والخدمات
- 💳 نظام الاشتراكات
- 🎁 نظام العروض

[📋 اطلع على سجل التغييرات الكامل](CHANGELOG.md)

---

## 🗺️ خارطة الطريق | Roadmap

### v2.2.0 (مارس 2026 - قريباً)
- [ ] تحديثات فورية للوحة التحكم
- [ ] تصدير للتقارير (PDF/Excel)
- [ ] أداة اختيار نطاق التواريخ
- [ ] نظام إشعارات البريد الإلكتروني
- [ ] فلاتر بحث متقدمة

### v2.3.0 (أبريل 2026)
- [ ] تطبيق موبايل (Flutter)
- [ ] بوابات دفع إلكتروني
- [ ] تكامل SMS
- [ ] تسجيل دخول عبر وسائل التواصل

### v3.0.0 (الربع الثاني 2026)
- [ ] نظام Multi-tenant
- [ ] حل White-label
- [ ] نظام تقارير متقدم
- [ ] توصيات مدعومة بالذكاء الاصطناعي

---

## 🤝 المساهمة | Contributing

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. Fork المستودع
2. أنشئ فرع للميزة الجديدة (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing-feature`)
5. افتح Pull Request

---

## 📝 الرخصة | License

هذا المشروع مرخص تحت رخصة MIT - اطلع على ملف [LICENSE](LICENSE) للتفاصيل.

MIT License - Free to use, modify, and distribute.

---

## 👨‍💻 المطور | Developer

**Sendoo M.**

- 🌐 GitHub: [@sendoo-m](https://github.com/sendoo-m)
- 📧 Email: [Contact via GitHub](https://github.com/sendoo-m)
- 💼 Portfolio: [Coming Soon]

---

## 💬 الدعم والمساعدة | Support

للاستفسارات والمساعدة:

- 🐛 **الإبلاغ عن أخطاء:** [GitHub Issues](https://github.com/sendoo-m/daliil-ay-khidma/issues)
- 💡 **طلبات الميزات:** [GitHub Discussions](https://github.com/sendoo-m/daliil-ay-khidma/discussions)
- 📧 **تواصل مباشر:** افتح Issue على GitHub

---

## 🌟 نشكرك على استخدام دليل أي خدمة!

**Thank you for using Daliil Ay Khidma!**

إذا أعجبك المشروع، لا تنسَ إعطاءه ⭐ على GitHub!

If you like this project, don't forget to give it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ in Egypt 🇪🇬**

**صُنع بحب في مصر**

[⬆ العودة للأعلى | Back to Top ⬆](#-دليل-أي-خدمة--daliil-ay-khidma)

</div>