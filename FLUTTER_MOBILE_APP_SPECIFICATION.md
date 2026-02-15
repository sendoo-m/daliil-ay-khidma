# 📱 مواصفات تطبيق الموبايل - دليل أي خدمة
## Flutter Mobile App Technical Specification

<div align="center">

**نسخة: 1.0**  
**تاريخ: فبراير 2026**  
**المشروع: دليل أي خدمة - Daliil Ay Khidma**

[العربية](#overview-ar) • [Technical Details](#technical-stack) • [API Integration](#api-integration)

</div>

---

## 📋 جدول المحتويات | Table of Contents

1. [نظرة عامة](#overview-ar)
2. [البنية التقنية](#technical-stack)
3. [الإصدارات المطلوبة](#versions)
4. [تكامل API](#api-integration)
5. [الميزات المطلوبة](#features)
6. [نماذج البيانات](#data-models)
7. [واجهات المستخدم](#ui-screens)
8. [المصادقة والأمان](#authentication)
9. [خطة التطوير](#development-plan)
10. [API غير المكتمل](#missing-apis)

---

## 🎯 نظرة عامة | Overview {#overview-ar}

### الهدف
تطوير **3 تطبيقات Flutter** منفصلة:

#### 1️⃣ **تطبيق المستخدم العام** (Public App)
**الجمهور المستهدف:** المستخدمين العاديين الباحثين عن محلات/منتجات/خدمات

**الميزات الرئيسية:**
- 🔍 بحث متقدم عن المحلات والخدمات
- 📍 خرائط وموقع جغرافي
- 🛒 تصفح المنتجات والخدمات
- ⭐ تقييم ومراجعة المحلات
- 💰 عرض العروض والخصومات
- ❤️ قائمة المفضلة
- 📱 مشاركة عبر وسائل التواصل
- 🌙 Dark/Light Mode
- 🌍 دعم العربية والإنجليزية

---

#### 2️⃣ **تطبيق لوحة التحكم للتجار** (Business Owner App)
**الجمهور المستهدف:** أصحاب المحلات + أصحاب الخدمات العامة

**الميزات الرئيسية:**
- 📊 **Dashboard** مع إحصائيات مباشرة:
  - عدد الزوار (Views)
  - النقرات (Clicks)
  - التقييمات (Reviews)
  - العروض النشطة (Active Deals)
  - المنتجات المباعة
- 📈 رسوم بيانية للأداء
- 🏪 إدارة المحلات:
  - إضافة/تعديل/حذف
  - رفع الصور
  - تحديث الموقع
- 🛒 إدارة المنتجات:
  - إضافة منتجات جديدة
  - تحديث الأسعار
  - إدارة المخزون
- 🎁 إدارة العروض:
  - إنشاء عروض جديدة
  - تتبع استخدام العروض
- 📋 إدارة التقييمات:
  - عرض التقييمات
  - الرد على التقييمات
- 🔔 الإشعارات:
  - تقييم جديد
  - طلب جديد
  - انتهاء العرض
- 💳 إدارة الاشتراك:
  - عرض الخطة الحالية
  - الترقية/التجديد

---

#### 3️⃣ **تطبيق الإدمن** (Admin App)
**الجمهور المستهدف:** فريق الإدارة (Admin Team)

**الميزات الرئيسية:**
- 🎛️ **Super Dashboard**:
  - إحصائيات عامة للنظام
  - عدد المستخدمين
  - عدد المحلات
  - عدد المنتجات
  - إيرادات الاشتراكات
- 👥 إدارة المستخدمين:
  - عرض/تعديل/حظر/حذف
  - تغيير الصلاحيات
- 🏢 إدارة المحلات:
  - الموافقة/الرفض
  - التحقق (Verification)
  - التمييز (Featured)
- ✅ مراجعة التقييمات:
  - الموافقة/الرفض على التقييمات
- 🎁 إدارة العروض:
  - الموافقة/الرفض على العروض
- 📊 تقارير متقدمة:
  - تقارير المبيعات
  - تقارير الأداء
  - تقارير الإيرادات
- 🔧 إعدادات النظام

---

## 🛠️ البنية التقنية | Technical Stack {#technical-stack}

### Frontend - Flutter
```yaml
Framework: Flutter 3.19+
Language: Dart 3.3+
Platforms: Android + iOS
Min SDK:
  - Android: 24 (Android 7.0)
  - iOS: 12.0
```

### Core Packages (مطلوب)
```yaml
# State Management
state_management:
  - provider: ^6.1.1         # إدارة الحالة
  - riverpod: ^2.4.10       # بديل متقدم
  # اختر واحد حسب تفضيلك

# Networking
networking:
  - dio: ^5.4.0             # HTTP Client
  - retrofit: ^4.0.3        # Type-safe REST client
  - pretty_dio_logger: ^1.3.1  # Logging

# Authentication
auth:
  - flutter_secure_storage: ^9.0.0  # تخزين Token آمن
  - jwt_decoder: ^2.0.1     # فك تشفير JWT

# Local Database
local_db:
  - sqflite: ^2.3.0         # SQLite
  - hive: ^2.2.3           # NoSQL (للكاش)
  - shared_preferences: ^2.2.2  # Key-Value storage

# UI Components
ui:
  - cached_network_image: ^3.3.1  # تحميل صور مع كاش
  - shimmer: ^3.0.0        # Loading placeholders
  - lottie: ^3.0.0         # Animations
  - flutter_svg: ^2.0.9    # SVG support
  - flutter_rating_bar: ^4.0.1  # Star ratings
  - carousel_slider: ^4.2.1  # صور منزلقة

# Maps & Location
maps:
  - google_maps_flutter: ^2.5.3  # خرائط
  - geolocator: ^11.0.0    # موقع المستخدم
  - geocoding: ^2.1.1      # تحويل إحداثيات

# Image Handling
images:
  - image_picker: ^1.0.7   # اختيار صور
  - image_cropper: ^5.0.1  # قص صور
  - flutter_image_compress: ^2.1.0  # ضغط صور

# Internationalization
i18n:
  - intl: ^0.19.0         # تنسيق التواريخ والأرقام
  - flutter_localizations: SDK  # دعم اللغات

# Utils
utils:
  - url_launcher: ^6.2.4   # فتح روابط خارجية
  - share_plus: ^7.2.1     # مشاركة محتوى
  - permission_handler: ^11.2.0  # صلاحيات
  - connectivity_plus: ^5.0.2  # فحص الاتصال
  - package_info_plus: ^5.0.1  # معلومات التطبيق

# Charts (للإحصائيات)
charts:
  - fl_chart: ^0.66.0      # رسوم بيانية
  - syncfusion_flutter_charts: ^24.2.8  # بديل متقدم

# Notifications
notifications:
  - firebase_messaging: ^14.7.10  # Push notifications
  - flutter_local_notifications: ^16.3.2  # إشعارات محلية

# Analytics (اختياري)
analytics:
  - firebase_analytics: ^10.8.0
  - firebase_crashlytics: ^3.4.9
```

---

## 🔌 تكامل API | API Integration {#api-integration}

### Base Configuration

#### API Base URL
```dart
// config/api_config.dart
class ApiConfig {
  // Development
  static const String DEV_BASE_URL = 'http://127.0.0.1:8008';
  
  // Production
  static const String PROD_BASE_URL = 'https://api.daliil-ay-khidma.com';
  
  // Current
  static const String BASE_URL = DEV_BASE_URL; // سيتغير حسب البيئة
  
  // API Version
  static const String API_VERSION = 'v2';
  
  // Full API URL
  static String get apiUrl => '$BASE_URL/api/$API_VERSION';
}
```

#### Dio Setup
```dart
// services/dio_client.dart
import 'package:dio/dio.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class DioClient {
  late Dio _dio;
  final _storage = FlutterSecureStorage();

  DioClient() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConfig.apiUrl,
        connectTimeout: Duration(seconds: 30),
        receiveTimeout: Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Accept-Language': 'ar', // ديناميكي حسب اللغة
        },
      ),
    );

    // Interceptors
    _dio.interceptors.add(PrettyDioLogger(
      requestHeader: true,
      requestBody: true,
      responseHeader: true,
    ));

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // إضافة Token
          final token = await _storage.read(key: 'access_token');
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (error, handler) async {
          // معالجة Token منتهي
          if (error.response?.statusCode == 401) {
            // حاول تحديث Token
            if (await _refreshToken()) {
              return handler.resolve(await _retry(error.requestOptions));
            }
          }
          return handler.next(error);
        },
      ),
    );
  }

  Dio get dio => _dio;

  Future<bool> _refreshToken() async {
    // TODO: Implement token refresh
    return false;
  }

  Future<Response<dynamic>> _retry(RequestOptions requestOptions) async {
    return await _dio.request<dynamic>(
      requestOptions.path,
      options: Options(
        method: requestOptions.method,
        headers: requestOptions.headers,
      ),
      data: requestOptions.data,
      queryParameters: requestOptions.queryParameters,
    );
  }
}
```

---

### 🔐 Authentication APIs {#authentication}

#### 1. Register
```dart
POST /api/v2/auth/register/

Request:
{
  "username": "ahmed123",
  "email": "ahmed@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "أحمد",
  "last_name": "محمد",
  "phone": "+201234567890"
}

Response 201:
{
  "user": {
    "id": 1,
    "username": "ahmed123",
    "email": "ahmed@example.com",
    "first_name": "أحمد",
    "last_name": "محمد",
    "phone": "+201234567890",
    "is_business_owner": false
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

#### 2. Login
```dart
POST /api/v2/auth/login/

Request:
{
  "username": "ahmed123",  // or email
  "password": "SecurePass123!"
}

Response 200:
{
  "user": { /* ... */ },
  "tokens": {
    "access": "...",
    "refresh": "..."
  }
}
```

#### 3. Refresh Token
```dart
POST /api/v2/auth/token/refresh/

Request:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 4. Get Current User
```dart
GET /api/v2/auth/me/
Authorization: Bearer {access_token}

Response 200:
{
  "id": 1,
  "username": "ahmed123",
  "email": "ahmed@example.com",
  "first_name": "أحمد",
  "last_name": "محمد",
  "phone": "+201234567890",
  "is_business_owner": false,
  "is_staff": false,
  "date_joined": "2026-02-15T20:00:00Z"
}
```

---

### 🏪 Business APIs (Public)

#### 1. List Businesses
```dart
GET /api/v2/businesses/

Query Parameters:
- page: int (default: 1)
- page_size: int (default: 20, max: 100)
- search: string (اسم المحل)
- category: int (ID الفئة)
- governorate: int
- city: int
- district: int
- type: string [retail, online, service, public_service, hybrid]
- is_verified: bool
- is_featured: bool
- ordering: string [name, created_at, -created_at, rating, -rating]

Response 200:
{
  "count": 150,
  "next": "http://api.../businesses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "slug": "pharmacy-mohamed-ali",
      "name_ar": "صيدلية محمد علي",
      "name_en": "Mohamed Ali Pharmacy",
      "category": {
        "id": 5,
        "name_ar": "صيدليات",
        "icon": "💊"
      },
      "logo": "https://api.../media/logos/pharmacy.jpg",
      "cover_image": "https://api.../media/covers/pharmacy-cover.jpg",
      "address_ar": "شارع الجمهورية، المنصورة",
      "district": {
        "id": 10,
        "name_ar": "الجامعة",
        "city": {
          "id": 2,
          "name_ar": "المنصورة",
          "governorate": {
            "id": 1,
            "name_ar": "الدقهلية"
          }
        }
      },
      "phone": "0501234567",
      "whatsapp": "201234567890",
      "latitude": 31.0409,
      "longitude": 31.3785,
      "rating_average": 4.5,
      "rating_count": 23,
      "view_count": 1520,
      "is_verified": true,
      "is_featured": false,
      "type": "retail",
      "created_at": "2026-01-15T10:30:00Z"
    }
    // ...
  ]
}
```

#### 2. Get Business Detail
```dart
GET /api/v2/businesses/{slug}/

Response 200:
{
  "id": 1,
  "slug": "pharmacy-mohamed-ali",
  "name_ar": "صيدلية محمد علي",
  "name_en": "Mohamed Ali Pharmacy",
  "description_ar": "صيدلية متكاملة توفر جميع الأدوية...",
  "description_en": "Complete pharmacy providing all medications...",
  "category": { /* ... */ },
  "logo": "https://...",
  "cover_image": "https://...",
  "images": [
    {
      "id": 1,
      "image": "https://api.../media/gallery/img1.jpg",
      "caption_ar": "واجهة الصيدلية",
      "order": 1
    }
  ],
  "address_ar": "شارع الجمهورية، المنصورة",
  "district": { /* ... */ },
  "phone": "0501234567",
  "whatsapp": "201234567890",
  "email": "info@pharmacy.com",
  "website": "https://pharmacy.com",
  "facebook": "https://facebook.com/pharmacy",
  "instagram": "https://instagram.com/pharmacy",
  "twitter": null,
  "tiktok": null,
  "working_hours_ar": "يومياً من 9 صباحاً حتى 11 مساءً",
  "latitude": 31.0409,
  "longitude": 31.3785,
  "rating_average": 4.5,
  "rating_count": 23,
  "view_count": 1520,
  "click_count": 340,
  "is_verified": true,
  "is_featured": false,
  "type": "retail",
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-02-10T14:20:00Z"
}
```

#### 3. Search Businesses
```dart
GET /api/v2/businesses/search/

Query Parameters:
- q: string (نص البحث)
- lat: float (موقع المستخدم)
- lng: float
- radius: int (بالكيلومتر، default: 5)
- category: int
- min_rating: float (1-5)

Response 200:
{
  "results": [
    {
      "business": { /* ... */ },
      "distance_km": 1.5,
      "relevance_score": 0.95
    }
  ]
}
```

---

### 🛒 Products APIs

#### 1. List Products
```dart
GET /api/v2/products/

Query Parameters:
- page, page_size
- search: string
- business: int (ID المحل)
- category: int
- type: string [product, service]
- min_price, max_price: decimal
- is_available: bool
- is_featured: bool
- ordering: string [name, price, -price, created_at, -created_at]

Response 200:
{
  "count": 500,
  "results": [
    {
      "id": 1,
      "slug": "panadol-extra-24-tablets",
      "name_ar": "بانادول إكسترا 24 قرص",
      "name_en": "Panadol Extra 24 Tablets",
      "description_ar": "مسكن قوي للصداع والآلام",
      "business": {
        "id": 1,
        "name_ar": "صيدلية محمد علي",
        "slug": "pharmacy-mohamed-ali"
      },
      "main_image": "https://api.../media/products/panadol.jpg",
      "images": [ /* ... */ ],
      "base_price": "45.00",
      "discounted_price": "42.50",
      "currency": "EGP",
      "type": "product",
      "is_available": true,
      "stock_quantity": 150,
      "is_featured": false,
      "created_at": "2026-02-01T10:00:00Z"
    }
  ]
}
```

---

### 🎁 Deals APIs

#### 1. List Deals
```dart
GET /api/v2/deals/

Query Parameters:
- page, page_size
- business: int
- type: string [percentage, fixed_amount, bogo, bundle]
- is_active: bool
- min_discount: int

Response 200:
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "title_ar": "خصم 20% على جميع المنتجات",
      "title_en": "20% Off All Products",
      "description_ar": "عرض محدود لمدة أسبوع",
      "business": { /* ... */ },
      "type": "percentage",
      "discount_value": "20.00",
      "start_date": "2026-02-15T00:00:00Z",
      "end_date": "2026-02-22T23:59:59Z",
      "usage_limit": 100,
      "used_count": 45,
      "is_active": true,
      "image": "https://api.../media/deals/deal1.jpg"
    }
  ]
}
```

---

### ⭐ Reviews APIs

#### 1. List Reviews
```dart
GET /api/v2/reviews/

Query Parameters:
- business: int (required)
- page, page_size
- rating: int (1-5)
- is_approved: bool
- ordering: string [created_at, -created_at, rating, -rating]

Response 200:
{
  "count": 23,
  "average_rating": 4.5,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 5,
        "username": "ahmed123",
        "full_name": "أحمد محمد"
      },
      "business": { /* ... */ },
      "rating": 5,
      "comment": "خدمة ممتازة والموظفين محترمين جداً",
      "is_approved": true,
      "created_at": "2026-02-10T15:30:00Z",
      "business_reply": "شكراً لك على تقييمك الرائع",
      "reply_date": "2026-02-10T18:00:00Z"
    }
  ]
}
```

#### 2. Add Review (Authentication Required)
```dart
POST /api/v2/reviews/
Authorization: Bearer {access_token}

Request:
{
  "business": 1,
  "rating": 5,
  "comment": "خدمة ممتازة"
}

Response 201:
{
  "id": 24,
  "user": { /* ... */ },
  "business": { /* ... */ },
  "rating": 5,
  "comment": "خدمة ممتازة",
  "is_approved": false,  // في انتظار موافقة الإدمن
  "created_at": "2026-02-15T20:30:00Z"
}
```

---

### ❤️ Favorites APIs (Authentication Required)

#### 1. List My Favorites
```dart
GET /api/v2/favorites/
Authorization: Bearer {access_token}

Response 200:
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "business": { /* business detail */ },
      "created_at": "2026-02-01T10:00:00Z"
    }
  ]
}
```

#### 2. Add to Favorites
```dart
POST /api/v2/favorites/
Authorization: Bearer {access_token}

Request:
{
  "business": 1
}

Response 201:
{
  "id": 6,
  "business": { /* ... */ },
  "created_at": "2026-02-15T20:35:00Z"
}
```

#### 3. Remove from Favorites
```dart
DELETE /api/v2/favorites/{id}/
Authorization: Bearer {access_token}

Response 204: No Content
```

---

### 📍 Location APIs

#### 1. List Governorates
```dart
GET /api/v2/locations/governorates/

Response 200:
[
  {
    "id": 1,
    "name_ar": "الدقهلية",
    "name_en": "Dakahlia",
    "is_active": true
  }
]
```

#### 2. List Cities
```dart
GET /api/v2/locations/cities/

Query Parameters:
- governorate: int (optional)

Response 200:
[
  {
    "id": 1,
    "name_ar": "المنصورة",
    "name_en": "Mansoura",
    "governorate": {
      "id": 1,
      "name_ar": "الدقهلية"
    },
    "is_active": true
  }
]
```

#### 3. List Districts
```dart
GET /api/v2/locations/districts/

Query Parameters:
- city: int (optional)
- governorate: int (optional)

Response 200:
[
  {
    "id": 1,
    "name_ar": "الجامعة",
    "name_en": "University",
    "city": {
      "id": 1,
      "name_ar": "المنصورة"
    },
    "is_active": true
  }
]
```

---

### 📊 Business Owner Dashboard APIs {#owner-apis}

**الصلاحية المطلوبة:** `is_business_owner = true`

#### 1. Get My Businesses
```dart
GET /api/v2/owner/businesses/
Authorization: Bearer {access_token}

Response 200:
[
  {
    "id": 1,
    "name_ar": "صيدلية محمد علي",
    "slug": "pharmacy-mohamed-ali",
    "stats": {
      "views": 1520,
      "clicks": 340,
      "rating_average": 4.5,
      "rating_count": 23,
      "products_count": 45,
      "deals_count": 3
    },
    "subscription": {
      "plan": "Premium",
      "expires_at": "2026-03-15T23:59:59Z",
      "is_active": true
    }
  }
]
```

#### 2. Get Business Statistics
```dart
GET /api/v2/owner/businesses/{id}/stats/
Authorization: Bearer {access_token}

Query Parameters:
- period: string [today, week, month, year]
- start_date, end_date: date (YYYY-MM-DD)

Response 200:
{
  "views": {
    "total": 1520,
    "chart_data": [
      {"date": "2026-02-01", "count": 45},
      {"date": "2026-02-02", "count": 52}
      // ...
    ]
  },
  "clicks": {
    "total": 340,
    "chart_data": [ /* ... */ ]
  },
  "reviews": {
    "total": 23,
    "average_rating": 4.5,
    "breakdown": {
      "5_star": 15,
      "4_star": 5,
      "3_star": 2,
      "2_star": 1,
      "1_star": 0
    }
  },
  "top_products": [
    {
      "product": { /* ... */ },
      "views": 250
    }
  ]
}
```

#### 3. Create/Update Business
```dart
POST /api/v2/owner/businesses/
PUT /api/v2/owner/businesses/{id}/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

Request:
{
  "name_ar": "صيدلية محمد علي",
  "name_en": "Mohamed Ali Pharmacy",
  "description_ar": "...",
  "category": 5,
  "district": 10,
  "address_ar": "...",
  "phone": "0501234567",
  "whatsapp": "201234567890",
  "latitude": 31.0409,
  "longitude": 31.3785,
  "logo": File,  // صورة
  "cover_image": File  // صورة
}

Response 201/200:
{ /* business detail */ }
```

#### 4. Manage Products
```dart
# List my products
GET /api/v2/owner/products/

# Create product
POST /api/v2/owner/products/

# Update product
PUT /api/v2/owner/products/{id}/

# Delete product
DELETE /api/v2/owner/products/{id}/
```

#### 5. Manage Deals
```dart
# List my deals
GET /api/v2/owner/deals/

# Create deal
POST /api/v2/owner/deals/

# Update deal
PUT /api/v2/owner/deals/{id}/

# Delete deal
DELETE /api/v2/owner/deals/{id}/
```

#### 6. Get My Reviews
```dart
GET /api/v2/owner/reviews/
Authorization: Bearer {access_token}

Query Parameters:
- business: int (optional)
- is_replied: bool

Response 200:
[
  {
    "id": 1,
    "user": { /* ... */ },
    "business": { /* ... */ },
    "rating": 5,
    "comment": "خدمة ممتازة",
    "created_at": "2026-02-10T15:30:00Z",
    "business_reply": null,
    "is_replied": false
  }
]
```

#### 7. Reply to Review
```dart
POST /api/v2/owner/reviews/{id}/reply/
Authorization: Bearer {access_token}

Request:
{
  "reply": "شكراً لك على تقييمك الرائع"
}

Response 200:
{
  "id": 1,
  "business_reply": "شكراً لك على تقييمك الرائع",
  "reply_date": "2026-02-15T20:40:00Z"
}
```

---

### 🎛️ Admin Dashboard APIs {#admin-apis}

**الصلاحية المطلوبة:** `is_staff = true` أو `is_superuser = true`

#### 1. System Overview
```dart
GET /api/v2/admin/overview/
Authorization: Bearer {access_token}

Response 200:
{
  "users": {
    "total": 1250,
    "active": 980,
    "business_owners": 145,
    "new_this_month": 67
  },
  "businesses": {
    "total": 450,
    "verified": 320,
    "pending_verification": 45,
    "active": 410
  },
  "products": {
    "total": 5600,
    "available": 4800
  },
  "deals": {
    "total": 125,
    "active": 78,
    "pending_approval": 12
  },
  "reviews": {
    "total": 2340,
    "pending_approval": 23
  },
  "revenue": {
    "total": "125000.00",
    "this_month": "15600.00",
    "currency": "EGP"
  }
}
```

#### 2. Manage Users
```dart
# List all users
GET /api/v2/admin/users/

# Get user detail
GET /api/v2/admin/users/{id}/

# Update user
PUT /api/v2/admin/users/{id}/

# Ban/Unban user
POST /api/v2/admin/users/{id}/toggle-active/

# Delete user
DELETE /api/v2/admin/users/{id}/
```

#### 3. Manage Businesses
```dart
# List all businesses
GET /api/v2/admin/businesses/

# Verify business
POST /api/v2/admin/businesses/{id}/verify/

# Feature business
POST /api/v2/admin/businesses/{id}/feature/

# Approve/Reject
POST /api/v2/admin/businesses/{id}/approve/
```

#### 4. Manage Reviews
```dart
# List pending reviews
GET /api/v2/admin/reviews/?is_approved=false

# Approve review
POST /api/v2/admin/reviews/{id}/approve/

# Reject/Delete review
DELETE /api/v2/admin/reviews/{id}/
```

#### 5. Reports
```dart
# Sales report
GET /api/v2/admin/reports/sales/

# Performance report
GET /api/v2/admin/reports/performance/

# Revenue report
GET /api/v2/admin/reports/revenue/
```

---

## ❌ APIs غير المكتملة (يجب تطويرها) {#missing-apis}

### 🔴 **High Priority** (ضروري للتطبيق)

#### 1. **Push Notifications API**
```dart
# تسجيل FCM Token
POST /api/v2/notifications/register-device/
Request:
{
  "fcm_token": "...",
  "device_type": "android",  // or "ios"
  "device_id": "unique-device-id"
}

# الحصول على الإشعارات
GET /api/v2/notifications/

# تحديد إشعار كمقروء
POST /api/v2/notifications/{id}/mark-read/
```

#### 2. **Subscription Management API**
```dart
# الحصول على خطط الاشتراك
GET /api/v2/subscriptions/plans/

# الاشتراك في خطة
POST /api/v2/subscriptions/subscribe/
Request:
{
  "plan": 2,  // Plan ID
  "period": "monthly",  // monthly, quarterly, semi_annual, annual
  "payment_method": "card"  // or "wallet", "bank_transfer"
}

# إلغاء الاشتراك
POST /api/v2/subscriptions/cancel/

# تجديد الاشتراك
POST /api/v2/subscriptions/renew/
```

#### 3. **Payment Gateway Integration**
```dart
# بوابة دفع (مثلاً: Paymob, Fawry, PayPal)
POST /api/v2/payments/checkout/
Request:
{
  "amount": "150.00",
  "currency": "EGP",
  "payment_method": "card",
  "subscription_id": 5
}

Response:
{
  "payment_url": "https://payment-gateway.com/checkout/...",
  "payment_id": "PAY-12345"
}

# تأكيد الدفع (Webhook)
POST /api/v2/payments/webhook/
```

#### 4. **Analytics API للإحصائيات المتقدمة**
```dart
# إحصائيات الزوار حسب الوقت
GET /api/v2/analytics/visitors/
Query: ?business=1&period=month

# تحليل الأداء
GET /api/v2/analytics/performance/

# تحليل المنافسين
GET /api/v2/analytics/competitors/
```

#### 5. **Chat/Messaging System** (اختياري ولكن مهم)
```dart
# إرسال رسالة لصاحب المحل
POST /api/v2/messages/send/
Request:
{
  "business": 1,
  "message": "هل المنتج متوفر؟"
}

# الحصول على المحادثات
GET /api/v2/messages/conversations/

# الحصول على رسائل محادثة
GET /api/v2/messages/conversations/{id}/
```

---

### 🟡 **Medium Priority** (مهم ولكن ليس عاجل)

#### 6. **Advanced Search with Filters**
```dart
POST /api/v2/search/advanced/
Request:
{
  "query": "صيدلية",
  "location": {
    "lat": 31.0409,
    "lng": 31.3785,
    "radius_km": 5
  },
  "filters": {
    "category": [5, 6],
    "min_rating": 4.0,
    "price_range": ["low", "medium"],
    "features": ["delivery", "24_hours"],
    "is_verified": true
  },
  "sort": "distance"  // or "rating", "popularity"
}
```

#### 7. **Deal Claims/Usage Tracking**
```dart
# استخدام عرض
POST /api/v2/deals/{id}/claim/
Authorization: Bearer {access_token}

Response:
{
  "claim_id": 123,
  "deal": { /* ... */ },
  "claimed_at": "2026-02-15T20:45:00Z",
  "expiry_date": "2026-02-22T23:59:59Z"
}

# عروضي المستخدمة
GET /api/v2/deals/my-claims/
```

#### 8. **Reports Export** (PDF/Excel)
```dart
GET /api/v2/owner/reports/export/
Query: ?format=pdf&period=month

Response: Binary file download
```

---

### 🟢 **Low Priority** (اختياري - يمكن إضافته لاحقاً)

#### 9. **Social Login** (Facebook, Google)
```dart
POST /api/v2/auth/social/google/
POST /api/v2/auth/social/facebook/
```

#### 10. **Recommendations Engine**
```dart
GET /api/v2/recommendations/
Query: ?based_on=favorites

Response:
{
  "businesses": [ /* ... */ ],
  "products": [ /* ... */ ]
}
```

---

## 📱 واجهات المستخدم المطلوبة {#ui-screens}

### تطبيق المستخدم العام (30+ شاشة)

#### Authentication
1. ✅ Splash Screen
2. ✅ Onboarding (3 شاشات)
3. ✅ Login
4. ✅ Register
5. ✅ Forgot Password
6. ✅ OTP Verification

#### Home
7. ✅ Home Screen
   - بانر مميز
   - فئات
   - محلات مميزة
   - عروض ساخنة
   - قريب منك
8. ✅ Category List
9. ✅ Business List (بالفلاتر)
10. ✅ Business Detail
11. ✅ Product Detail
12. ✅ Deal Detail

#### Search
13. ✅ Search Screen
14. ✅ Advanced Search Filters
15. ✅ Map View

#### Profile
16. ✅ My Profile
17. ✅ Edit Profile
18. ✅ My Favorites
19. ✅ My Reviews
20. ✅ Settings
21. ✅ Language Settings
22. ✅ Theme Settings
23. ✅ Notifications Settings

#### Reviews
24. ✅ Reviews List
25. ✅ Add Review

#### Other
26. ✅ About Us
27. ✅ Contact Us
28. ✅ Privacy Policy
29. ✅ Terms of Service
30. ✅ No Internet Screen

---

### تطبيق لوحة التحكم (40+ شاشة)

#### Dashboard
1. ✅ Dashboard Home
   - إحصائيات
   - رسوم بيانية
   - إشعارات
2. ✅ Analytics Details

#### My Businesses
3. ✅ Business List
4. ✅ Business Detail
5. ✅ Add Business
6. ✅ Edit Business
7. ✅ Business Images Gallery
8. ✅ Business Location (Map)

#### Products
9. ✅ Product List
10. ✅ Product Detail
11. ✅ Add Product
12. ✅ Edit Product
13. ✅ Product Images
14. ✅ Stock Management

#### Deals
15. ✅ Deal List
16. ✅ Deal Detail
17. ✅ Create Deal
18. ✅ Edit Deal
19. ✅ Deal Usage Statistics

#### Reviews
20. ✅ Reviews List
21. ✅ Review Detail
22. ✅ Reply to Review

#### Subscription
23. ✅ My Subscription
24. ✅ Plans List
25. ✅ Upgrade Plan
26. ✅ Payment History

#### Reports
27. ✅ Performance Report
28. ✅ Visitors Report
29. ✅ Sales Report
30. ✅ Export Reports

#### Notifications
31. ✅ Notifications List
32. ✅ Notification Settings

#### Profile
33. ✅ My Profile
34. ✅ Edit Profile
35. ✅ Change Password
36. ✅ Settings

---

### تطبيق الإدمن (50+ شاشة)

#### Super Dashboard
1. ✅ Admin Dashboard
   - إحصائيات النظام
   - رسوم بيانية متقدمة
2. ✅ System Health

#### Users Management
3. ✅ Users List
4. ✅ User Detail
5. ✅ Edit User
6. ✅ User Permissions
7. ✅ Ban/Unban User

#### Businesses Management
8. ✅ All Businesses List
9. ✅ Pending Verification
10. ✅ Verify Business
11. ✅ Feature Business
12. ✅ Moderate Business

#### Products Management
13. ✅ All Products
14. ✅ Moderate Product

#### Deals Management
15. ✅ All Deals
16. ✅ Pending Approval
17. ✅ Approve/Reject Deal

#### Reviews Management
18. ✅ All Reviews
19. ✅ Pending Reviews
20. ✅ Approve/Reject Review
21. ✅ Flagged Reviews

#### Reports
22. ✅ Users Report
23. ✅ Businesses Report
24. ✅ Revenue Report
25. ✅ Performance Report
26. ✅ Custom Reports

#### Settings
27. ✅ System Settings
28. ✅ Categories Management
29. ✅ Locations Management
30. ✅ Plans Management

---

## 🔐 Security & Best Practices

### 1. Token Storage
```dart
// استخدم flutter_secure_storage
final storage = FlutterSecureStorage();

// حفظ Token
await storage.write(key: 'access_token', value: token);

// قراءة Token
final token = await storage.read(key: 'access_token');
```

### 2. Error Handling
```dart
try {
  final response = await dio.get('/businesses/');
  return response.data;
} on DioException catch (e) {
  if (e.response?.statusCode == 401) {
    // Token expired - refresh or logout
  } else if (e.response?.statusCode == 404) {
    // Not found
  } else {
    // Other errors
  }
  throw Exception(e.message);
}
```

### 3. Caching Strategy
- استخدم `Hive` للكاش المحلي
- Cache المحافظات/المدن/الأحياء (نادراً ما تتغير)
- Cache آخر نتائج البحث
- Refresh كل 30 دقيقة

### 4. Image Optimization
```dart
// استخدم cached_network_image
CachedNetworkImage(
  imageUrl: business.logo,
  placeholder: (context, url) => Shimmer(...),
  errorWidget: (context, url, error) => Icon(Icons.error),
  cacheManager: CustomCacheManager(),
);
```

---

## 📅 خطة التطوير المقترحة {#development-plan}

### المرحلة 1: الإعداد والبنية (أسبوع 1)
- ✅ إعداد Flutter project
- ✅ تثبيت Dependencies
- ✅ إعداد State Management
- ✅ إعداد API Client (Dio)
- ✅ إعداد Routing
- ✅ إعداد Theme (Dark/Light)
- ✅ إعداد Localization (AR/EN)

### المرحلة 2: Authentication (أسبوع 2)
- ✅ Splash Screen
- ✅ Onboarding
- ✅ Login/Register
- ✅ Token Management
- ✅ Auto-login

### المرحلة 3: تطبيق المستخدم - الأساسيات (أسبوع 3-4)
- ✅ Home Screen
- ✅ Business List
- ✅ Business Detail
- ✅ Search
- ✅ Map Integration
- ✅ Favorites

### المرحلة 4: تطبيق المستخدم - الميزات المتقدمة (أسبوع 5)
- ✅ Product List/Detail
- ✅ Deals
- ✅ Reviews (عرض + إضافة)
- ✅ Profile & Settings

### المرحلة 5: تطبيق التجار - Dashboard (أسبوع 6-7)
- ✅ Dashboard Home
- ✅ Analytics
- ✅ Business Management
- ✅ Product Management
- ✅ Deal Management

### المرحلة 6: تطبيق التجار - إكمال (أسبوع 8)
- ✅ Reviews Management
- ✅ Subscription Management
- ✅ Reports
- ✅ Notifications

### المرحلة 7: تطبيق الإدمن (أسبوع 9-10)
- ✅ Admin Dashboard
- ✅ Users Management
- ✅ Businesses Moderation
- ✅ Reviews Moderation
- ✅ Reports

### المرحلة 8: Testing & Deployment (أسبوع 11-12)
- ✅ Unit Tests
- ✅ Integration Tests
- ✅ UI Tests
- ✅ Bug Fixes
- ✅ Performance Optimization
- ✅ Play Store & App Store Submission

---

## 📞 اتصال وتنسيق

### الملفات المطلوبة من Backend

1. **Postman Collection** لجميع APIs
2. **Swagger/OpenAPI** Documentation
3. **Example Responses** لكل endpoint
4. **Error Codes** المستخدمة
5. **FCM Server Key** للإشعارات
6. **API Base URL** (Development + Production)
7. **Test Accounts**:
   - مستخدم عادي
   - صاحب محل
   - إدمن

### التواصل المستمر
- Weekly sync meetings
- Shared Trello/Jira board
- API changes notification
- Bug tracking system

---

## 🎯 الخلاصة

النظام **جاهز تقريباً** لتطوير Flutter، لكن يحتاج:

### ✅ موجود وجاهز:
- Authentication APIs
- Business APIs (CRUD)
- Product APIs
- Deal APIs
- Review APIs
- Location APIs
- Favorites APIs

### ⚠️ يحتاج تطوير:
- **Push Notifications API** ⭐ (أولوية عالية)
- **Subscription Management API** ⭐
- **Payment Gateway Integration** ⭐
- **Analytics API** (للإحصائيات المتقدمة)
- **Chat/Messaging** (اختياري)
- **Advanced Search** (يمكن البدء بالبسيط)
- **Deal Claims Tracking**

### 📊 تقييم الجاهزية:
**75% - 80%** من APIs جاهزة ✅  
**20% - 25%** تحتاج تطوير ⚠️

---

**مدة التطوير المتوقعة:** 10-12 أسبوع  
**الفريق المطلوب:** 2-3 Flutter Developers  
**Backend Support:** متاح حسب الحاجة

---

<div align="center">

**🚀 جاهزين للبدء! 🚀**

لأي استفسارات أو توضيحات، يُرجى التواصل

**Made with ❤️ for Daliil Ay Khidma**

</div>
