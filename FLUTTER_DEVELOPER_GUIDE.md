# 📱 Daliil Ay Khidma - دليل مطور Flutter

## 📋 نظرة عامة على المشروع

**دليل أي خدمة** - منصة شاملة للبحث عن المحلات، المنتجات، العروض، والخدمات العامة في مصر.

### 🎯 نطاق التطبيق المطلوب

تطوير **3 تطبيقات Flutter** منفصلة:

1. **📱 تطبيق المستخدم (Public App)** - للجمهور العادي
2. **💼 تطبيق أصحاب المحلات (Business Owner App)** - لإدارة المحلات والمنتجات
3. **🔧 تطبيق الإدارة (Admin App)** - للمشرفين وفريق العمل

---

## 🏗️ البنية المعمارية للنظام

### 📊 قاعدة البيانات - الكيانات الرئيسية

```
┌─────────────────────┐
│     Users           │
│  (accounts app)     │
├─────────────────────┤
│ - id                │
│ - username          │
│ - email             │
│ - phone             │
│ - is_staff          │
│ - is_verified       │
└─────────────────────┘
         │
         ├─── يمتلك (owner) ──┐
         │                     │
         │                     ▼
         │         ┌─────────────────────┐
         │         │    Business         │
         │         │  (directory app)    │
         │         ├─────────────────────┤
         │         │ - id, slug          │
         │         │ - name_ar/en        │
         │         │ - description       │
         │         │ - category          │
         │         │ - location (lat/lng)│
         │         │ - phone, whatsapp   │
         │         │ - logo, images      │
         │         │ - is_verified       │
         │         │ - is_featured       │
         │         │ - view_count        │
         │         │ - type (business/   │
         │         │   service)          │
         │         └─────────────────────┘
         │                     │
         │                     ├── يحتوي على ──┐
         │                     │                │
         │                     ▼                ▼
         │         ┌─────────────────┐  ┌─────────────────┐
         │         │   Products      │  │     Deals       │
         │         ├─────────────────┤  ├─────────────────┤
         │         │ - id, slug      │  │ - id            │
         │         │ - name_ar/en    │  │ - title_ar/en   │
         │         │ - price         │  │ - discount_%    │
         │         │ - discount      │  │ - start/end_date│
         │         │ - images        │  │ - is_active     │
         │         │ - is_available  │  │ - usage_count   │
         │         └─────────────────┘  └─────────────────┘
         │
         └─── يقيّم ────┐
                        ▼
              ┌─────────────────┐
              │    Reviews      │
              ├─────────────────┤
              │ - id            │
              │ - user          │
              │ - business      │
              │ - rating (1-5)  │
              │ - comment       │
              │ - is_approved   │
              └─────────────────┘

┌─────────────────────┐
│   Categories        │
├─────────────────────┤
│ - id                │
│ - name_ar/en        │
│ - icon              │
│ - parent (nested)   │
└─────────────────────┘

┌─────────────────────┐
│   Locations         │
├─────────────────────┤
│ Governorate         │
│   └─ City           │
│       └─ District   │
└─────────────────────┘

┌─────────────────────┐
│  Subscriptions      │
├─────────────────────┤
│ - Plans             │
│ - Features          │
│ - User Subs         │
└─────────────────────┘
```

---

## 🔌 REST API - الموجود حالياً

### ✅ APIs الجاهزة (v1)

**Base URL:** `http://your-domain.com/api/v1/`

#### 🔐 Authentication (JWT)
```
POST   /api/v1/auth/login/
POST   /api/v1/auth/register/
POST   /api/v1/auth/refresh/
GET    /api/v1/auth/profile/
PUT    /api/v1/auth/profile/update/
POST   /api/v1/auth/change-password/
```

#### 📂 Categories
```
GET    /api/v1/categories/
GET    /api/v1/categories/{id}/
```

#### 🏢 Businesses (محلات وخدمات)
```
GET    /api/v1/businesses/
       Query Params:
         - search: البحث في الاسم والوصف
         - category: فلترة حسب الفئة
         - city: فلترة حسب المدينة
         - is_verified: فقط الموثقة
         - type: business أو service
         - page, page_size: pagination

GET    /api/v1/businesses/{id}/
POST   /api/v1/businesses/          [Auth Required]
PUT    /api/v1/businesses/{id}/     [Owner Only]
DELETE /api/v1/businesses/{id}/     [Owner Only]
```

#### 📦 Products
```
GET    /api/v1/products/
GET    /api/v1/products/{id}/
POST   /api/v1/products/             [Auth Required]
PUT    /api/v1/products/{id}/        [Owner Only]
DELETE /api/v1/products/{id}/        [Owner Only]
```

#### 🎁 Deals (العروض)
```
GET    /api/v1/deals/
GET    /api/v1/deals/{id}/
POST   /api/v1/deals/                [Auth Required]
PUT    /api/v1/deals/{id}/           [Owner Only]
DELETE /api/v1/deals/{id}/           [Owner Only]
POST   /api/v1/deals/{id}/use/       [Auth Required]
```

#### ⭐ Favorites (المفضلة)
```
GET    /api/v1/favorites/            [Auth Required]
POST   /api/v1/favorites/            [Auth Required]
DELETE /api/v1/favorites/{id}/       [Auth Required]
```

#### 📍 Locations
```
GET    /api/v1/governorates/
GET    /api/v1/cities/
GET    /api/v1/districts/
```

#### 💳 Subscriptions
```
GET    /api/v1/subscription-plans/
GET    /api/v1/subscriptions/        [Auth Required]
POST   /api/v1/subscriptions/        [Auth Required]
```

---

## ⚠️ APIs المطلوب تطويرها

### 🔴 High Priority - ضروري لتطبيق المستخدم

#### 1️⃣ Reviews API (مكتمل جزئياً - يحتاج تحسين)
```
✅ GET    /api/v1/reviews/?business={id}
❌ POST   /api/v1/reviews/              [Auth Required]
❌ PUT    /api/v1/reviews/{id}/         [Owner Only]
❌ DELETE /api/v1/reviews/{id}/         [Owner/Admin Only]
❌ POST   /api/v1/reviews/{id}/reply/   [Business Owner]
```

#### 2️⃣ Search & Filter API (محتاج تطوير)
```
❌ GET    /api/v1/search/
       Query Params:
         - q: البحث الشامل
         - type: business, product, deal, service
         - category
         - location (lat, lng, radius)
         - price_min, price_max
         - sort: relevance, rating, views, created
```

#### 3️⃣ Business Statistics (للخريطة والفلترة)
```
❌ GET    /api/v1/businesses/nearby/
       Query Params:
         - lat, lng, radius (km)
         - category
         - limit
```

---

### 🟡 Medium Priority - لتطبيق أصحاب المحلات

#### 4️⃣ Business Owner Dashboard API
```
❌ GET    /api/v1/owner/dashboard/
       Response:
         - total_views
         - total_reviews
         - average_rating
         - total_favorites
         - active_deals
         - products_count

❌ GET    /api/v1/owner/businesses/
       جميع محلات المالك

❌ GET    /api/v1/owner/statistics/
       Query Params:
         - business_id
         - start_date, end_date
       Response:
         - views_over_time []
         - top_products []
         - review_stats {}
```

#### 5️⃣ Product Management APIs
```
❌ PATCH  /api/v1/products/{id}/toggle-availability/
❌ POST   /api/v1/products/bulk-update/
       Body: [{id, price, discount}, ...]
```

#### 6️⃣ Deal Management APIs
```
❌ GET    /api/v1/owner/deals/analytics/
       Response:
         - deal_id
         - views
         - usage_count
         - conversion_rate
```

#### 7️⃣ Reviews Management
```
❌ GET    /api/v1/owner/reviews/
       جميع تقييمات محلات المالك
       
❌ POST   /api/v1/owner/reviews/{id}/respond/
       الرد على التقييمات
```

---

### 🟢 Low Priority - لتطبيق الإدارة (Admin)

#### 8️⃣ Admin Dashboard API
```
❌ GET    /api/v1/admin/dashboard/
       Response:
         - total_businesses
         - total_users
         - total_products
         - total_deals
         - pending_verifications
         - recent_registrations []

❌ GET    /api/v1/admin/statistics/
       Query Params:
         - period: today, week, month, year
       Response:
         - users_growth []
         - businesses_growth []
         - revenue_stats {}
```

#### 9️⃣ Admin Management APIs
```
✅ GET    /api/v2/admin/users/
✅ GET    /api/v2/admin/businesses/
❌ POST   /api/v2/admin/businesses/{id}/verify/
❌ POST   /api/v2/admin/businesses/{id}/feature/
❌ POST   /api/v2/admin/reviews/{id}/approve/
❌ POST   /api/v2/admin/reviews/{id}/reject/
```

#### 🔟 Notifications API (مستقبلي)
```
❌ GET    /api/v1/notifications/
❌ POST   /api/v1/notifications/{id}/mark-read/
❌ POST   /api/v1/notifications/mark-all-read/
```

---

## 📱 تطبيق المستخدم (Public App) - التفاصيل

### 🎨 الشاشات الرئيسية

#### 1. الصفحة الرئيسية (Home)
```dart
// Features:
- شريط البحث (Search Bar)
- الفئات (Categories Grid)
- محلات مميزة (Featured Businesses)
- عروض حصرية (Hot Deals)
- خدمات عامة (Public Services)

// APIs Needed:
GET /api/v1/categories/
GET /api/v1/businesses/?is_featured=true&page_size=10
GET /api/v1/deals/?is_active=true&page_size=5
GET /api/v1/businesses/?type=service&page_size=10
```

#### 2. البحث والفلترة (Search & Filter)
```dart
// Features:
- بحث شامل (Full-text search)
- فلترة حسب الفئة
- فلترة حسب الموقع
- فلترة حسب التقييم
- ترتيب النتائج

// APIs Needed:
❌ GET /api/v1/search/?q=...&category=...&city=...
GET /api/v1/businesses/?search=...&category=...
```

#### 3. تفاصيل المحل (Business Detail)
```dart
// Features:
- معلومات المحل الكاملة
- الموقع على الخريطة (Google Maps)
- قائمة المنتجات
- العروض الحالية
- التقييمات والمراجعات
- أزرار الاتصال (اتصال، واتساب، الاتجاهات)
- إضافة للمفضلة

// APIs Needed:
GET /api/v1/businesses/{id}/
GET /api/v1/products/?business={id}
GET /api/v1/deals/?business={id}
❌ GET /api/v1/reviews/?business={id}
```

#### 4. التصنيفات (Categories)
```dart
// Features:
- عرض كل الفئات
- الفئات الفرعية
- عدد المحلات في كل فئة

// APIs Needed:
GET /api/v1/categories/
GET /api/v1/businesses/?category={id}
```

#### 5. الخريطة (Map View)
```dart
// Features:
- عرض المحلات على الخريطة
- فلترة حسب الموقع الحالي
- عرض المحلات القريبة

// APIs Needed:
❌ GET /api/v1/businesses/nearby/?lat=...&lng=...&radius=5
GET /api/v1/businesses/?page_size=100  // مع coordinates
```

#### 6. المفضلة (Favorites)
```dart
// Features:
- قائمة المحلات المفضلة
- إزالة من المفضلة

// APIs Needed:
GET /api/v1/favorites/
POST /api/v1/favorites/ {business_id}
DELETE /api/v1/favorites/{id}/
```

#### 7. الملف الشخصي (Profile)
```dart
// Features:
- معلومات المستخدم
- تعديل البيانات
- تغيير كلمة المرور
- سجل التقييمات

// APIs Needed:
GET /api/v1/auth/profile/
PUT /api/v1/auth/profile/update/
POST /api/v1/auth/change-password/
```

---

## 💼 تطبيق أصحاب المحلات - التفاصيل

### 🎨 الشاشات الرئيسية

#### 1. لوحة التحكم (Dashboard)
```dart
// Features:
- إحصائيات سريعة:
  * عدد المشاهدات (Views)
  * عدد التقييمات (Reviews)
  * متوسط التقييم (Rating)
  * عدد المفضلة (Favorites)
- رسم بياني للمشاهدات
- آخر التقييمات
- العروض النشطة

// APIs Needed:
❌ GET /api/v1/owner/dashboard/
❌ GET /api/v1/owner/statistics/?period=week
```

#### 2. إدارة المحلات (My Businesses)
```dart
// Features:
- قائمة محلاتي
- إضافة محل جديد
- تعديل بيانات المحل
- رفع الصور
- تحديد الموقع على الخريطة

// APIs Needed:
❌ GET /api/v1/owner/businesses/
POST /api/v1/businesses/
PUT /api/v1/businesses/{id}/
DELETE /api/v1/businesses/{id}/
```

#### 3. إدارة المنتجات (Products)
```dart
// Features:
- قائمة المنتجات
- إضافة منتج
- تعديل السعر والخصم
- تفعيل/إيقاف المنتج
- تحديث متعدد (Bulk Update)

// APIs Needed:
GET /api/v1/products/?business={id}
POST /api/v1/products/
PUT /api/v1/products/{id}/
❌ PATCH /api/v1/products/{id}/toggle-availability/
❌ POST /api/v1/products/bulk-update/
```

#### 4. إدارة العروض (Deals)
```dart
// Features:
- قائمة العروض
- إضافة عرض جديد
- تحديد مدة العرض
- إحصائيات العرض (مشاهدات، استخدام)

// APIs Needed:
GET /api/v1/deals/?business={id}
POST /api/v1/deals/
PUT /api/v1/deals/{id}/
❌ GET /api/v1/owner/deals/analytics/
```

#### 5. التقييمات (Reviews)
```dart
// Features:
- عرض كل التقييمات
- الرد على التقييمات
- فلترة حسب التقييم

// APIs Needed:
❌ GET /api/v1/owner/reviews/
❌ POST /api/v1/owner/reviews/{id}/respond/
```

#### 6. الإحصائيات (Statistics)
```dart
// Features:
- رسم بياني للمشاهدات
- أكثر المنتجات مشاهدة
- توزيع التقييمات
- تقرير مفصل

// APIs Needed:
❌ GET /api/v1/owner/statistics/?start_date=...&end_date=...
```

---

## 🔧 تطبيق الإدارة (Admin App) - التفاصيل

### 🎨 الشاشات الرئيسية

#### 1. لوحة التحكم الرئيسية
```dart
// Features:
- إجمالي المحلات
- إجمالي المستخدمين
- المحلات في انتظار التوثيق
- إحصائيات النمو

// APIs Needed:
❌ GET /api/v1/admin/dashboard/
❌ GET /api/v1/admin/statistics/?period=month
```

#### 2. إدارة المستخدمين
```dart
// Features:
- قائمة المستخدمين
- حظر/تفعيل مستخدم
- عرض تفاصيل المستخدم

// APIs Needed:
✅ GET /api/v2/admin/users/
❌ POST /api/v2/admin/users/{id}/toggle-active/
```

#### 3. إدارة المحلات
```dart
// Features:
- قائمة جميع المحلات
- توثيق المحلات
- جعل المحل مميز
- حذف محل

// APIs Needed:
✅ GET /api/v2/admin/businesses/
❌ POST /api/v2/admin/businesses/{id}/verify/
❌ POST /api/v2/admin/businesses/{id}/feature/
❌ DELETE /api/v2/admin/businesses/{id}/
```

#### 4. إدارة التقييمات
```dart
// Features:
- عرض كل التقييمات
- الموافقة/الرفض
- حذف تقييم

// APIs Needed:
❌ GET /api/v2/admin/reviews/
❌ POST /api/v2/admin/reviews/{id}/approve/
❌ POST /api/v2/admin/reviews/{id}/reject/
❌ DELETE /api/v2/admin/reviews/{id}/
```

#### 5. التقارير والإحصائيات
```dart
// Features:
- تقارير شاملة
- تصدير بيانات
- رسوم بيانية متقدمة

// APIs Needed:
❌ GET /api/v1/admin/reports/?type=...&period=...
```

---

## 🔧 التقنيات المطلوبة (Flutter)

### 📦 Packages الأساسية

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.0.0          # أو riverpod أو bloc
  
  # Networking
  dio: ^5.0.0              # HTTP client
  retrofit: ^4.0.0         # Type-safe API calls
  
  # Local Storage
  shared_preferences: ^2.2.0
  hive: ^2.2.0             # للكاش
  
  # Authentication
  flutter_secure_storage: ^9.0.0  # تخزين Token
  
  # UI Components
  cached_network_image: ^3.3.0
  shimmer: ^3.0.0          # Loading skeleton
  flutter_rating_bar: ^4.0.0
  
  # Maps & Location
  google_maps_flutter: ^2.5.0
  geolocator: ^10.0.0
  geocoding: ^2.1.0
  
  # Utils
  intl: ^0.18.0            # للتاريخ والعملات
  url_launcher: ^6.2.0     # فتح روابط وأرقام
  image_picker: ^1.0.0     # رفع صور
  
  # Charts (للإحصائيات)
  fl_chart: ^0.66.0
```

### 🏗️ البنية المقترحة

```
lib/
├── core/
│   ├── api/
│   │   ├── api_client.dart
│   │   ├── api_endpoints.dart
│   │   └── dio_interceptor.dart
│   ├── models/
│   │   ├── user.dart
│   │   ├── business.dart
│   │   ├── product.dart
│   │   ├── deal.dart
│   │   └── review.dart
│   ├── services/
│   │   ├── auth_service.dart
│   │   ├── storage_service.dart
│   │   └── location_service.dart
│   └── utils/
│       ├── constants.dart
│       └── helpers.dart
│
├── features/
│   ├── auth/
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── providers/
│   ├── home/
│   ├── search/
│   ├── business/
│   ├── favorites/
│   └── profile/
│
├── shared/
│   ├── widgets/
│   └── themes/
│
└── main.dart
```

---

## 🎯 خطة التنفيذ المقترحة

### المرحلة 1️⃣ - تطوير APIs المطلوبة (أسبوعين)
✅ Backend Developer
1. Reviews API كاملة
2. Search & Filter API
3. Owner Dashboard API
4. Admin Management APIs
5. Statistics APIs

### المرحلة 2️⃣ - تطبيق المستخدم (3 أسابيع)
📱 Flutter Developer
1. Setup & Authentication
2. Home & Categories
3. Search & Filter
4. Business Details
5. Map Integration
6. Favorites & Profile
7. Testing

### المرحلة 3️⃣ - تطبيق أصحاب المحلات (2 أسبوع)
💼 Flutter Developer
1. Dashboard
2. Business Management
3. Products & Deals
4. Reviews Management
5. Statistics

### المرحلة 4️⃣ - تطبيق الإدارة (أسبوع)
🔧 Flutter Developer
1. Admin Dashboard
2. User Management
3. Business Management
4. Reviews Moderation

### المرحلة 5️⃣ - Testing & Launch (أسبوع)
🚀 Team
1. Integration Testing
2. Bug Fixes
3. Performance Optimization
4. Play Store & App Store Submission

**إجمالي الوقت المتوقع: 8-9 أسابيع**

---

## 📞 للتواصل

أي استفسارات أو توضيحات إضافية، تواصل مع فريق Backend!

---

**تاريخ الإنشاء:** 15 فبراير 2026  
**الإصدار:** 1.0  
**الحالة:** ✅ جاهز للتطوير
