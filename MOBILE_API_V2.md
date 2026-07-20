# Mobile API v2

القاعدة الأساسية لكل نقاط الموبايل:

```text
/api/v2/
```

التوثيق التفاعلي:

```text
Swagger: /api/v2/docs/
ReDoc:   /api/v2/redoc/
Schema:  /api/v2/schema/
```

تطبق الخدمة الحدود الافتراضية التالية:

```text
Anonymous:      300 request/hour
Authenticated: 3000 request/hour
Login/refresh: 10 request/minute
Registration:  5 request/hour
Password reset: 5 request/hour
```

## المصادقة

ترسل الطلبات المحمية Access Token في الترويسة:

```http
Authorization: Bearer <access-token>
```

| العملية | Method | Endpoint | الحماية |
|---|---|---|---|
| إنشاء حساب | POST | `auth/register/` | عام |
| تسجيل الدخول | POST | `auth/login/` | عام |
| تجديد الرمز | POST | `auth/refresh/` | Refresh Token |
| تسجيل الخروج | POST | `auth/logout/` | Access Token |
| الملف الشخصي | GET | `auth/profile/` | Access Token |
| تعديل الملف | PUT/PATCH | `auth/profile/update/` | Access Token |
| تغيير كلمة المرور | POST | `auth/change-password/` | Access Token |
| طلب الاستعادة | POST | `auth/password-reset/` | عام |
| تأكيد الاستعادة | POST | `auth/password-reset/confirm/` | عام |

### تسجيل الخروج

```json
{
  "refresh": "<refresh-token>"
}
```

بعد نجاح الطلب لا يمكن استخدام Refresh Token مرة أخرى.

### استعادة كلمة المرور

طلب إرسال البريد:

```json
{
  "email": "user@example.com"
}
```

الرابط المرسل يستخدم القيمة المعرفة في متغير البيئة:

```env
MOBILE_PASSWORD_RESET_URL=daliil://reset-password
```

يرسل تطبيق Flutter القيمتين `uid` و`token` الموجودتين في الرابط مع كلمة المرور الجديدة:

```json
{
  "uid": "...",
  "token": "...",
  "password": "NewStrongPassword123!",
  "password_confirm": "NewStrongPassword123!"
}
```

## صلاحيات الأدوار

- المستخدم: النقاط العامة، الملف الشخصي، المفضلة، التقييمات والمطالبات بالعروض.
- صاحب النشاط: المسارات التي تبدأ بـ `business-owner/` وبيانات أنشطته فقط.
- المدير: المسارات التي تبدأ بـ `admin/`.

## فصل العرض العام عن الإدارة

المسارات العامة التالية للقراءة فقط، ولا تقبل POST أو PUT أو PATCH أو DELETE:

```text
businesses/
products/
deals/
```

إنشاء وتعديل وحذف بيانات صاحب النشاط يتم فقط من خلال:

```text
business-owner/businesses/
business-owner/businesses/{business_id}/products/
business-owner/businesses/{business_id}/deals/
```

## رفع الصور

تقبل الواجهات صور JPEG وPNG وWebP بحد أقصى 5 ميجابايت للصورة، وبحد أقصى 10 صور لكل معرض.

```text
GET/POST business-owner/businesses/{business_id}/images/
DELETE   business-owner/businesses/{business_id}/images/{image_id}/

GET/POST business-owner/businesses/{business_id}/products/{product_id}/images/
DELETE   business-owner/businesses/{business_id}/products/{product_id}/images/{image_id}/
```

ترسل الصور باستخدام `multipart/form-data` في حقل اسمه `image`.

## الصفحة الرئيسية والبحث

يجمع endpoint الصفحة الرئيسية أقسام التطبيق الأساسية في طلب واحد:

```text
GET home/
```

ويعيد التصنيفات، الأنشطة المميزة، المنتجات المميزة، العروض المميزة والمحافظات.

يدعم دليل الأنشطة معاملات البحث التالية:

```text
GET businesses/?search=مطعم
GET businesses/?governorate=1&city=2&district=3
GET businesses/?category=4&business_type=shop&min_rating=4
GET businesses/?ordering=-average_rating
```

وتدعم المنتجات السعر والموقع والتصنيف:

```text
GET products/?category=4&min_price=100&max_price=500
GET products/?governorate=1&city=2&district=3
```

البحث عن أقرب الأنشطة:

```text
GET businesses/nearby/?latitude=30.0444&longitude=31.2357&radius_km=20
```

نطاق البحث الجغرافي المسموح من أكبر من صفر وحتى 100 كم، ويعيد بحد أقصى 20 نشاطًا مرتبة حسب `distance_km`.

## تفاعلات المستخدم

### المفضلة

```text
GET  favorites/
POST favorites/toggle/
```

```json
{
  "business_id": 123
}
```

لا يمكن إضافة نشاط غير منشور أو غير معتمد إلى المفضلة.

### التقييمات

```text
GET    reviews/?business=123
POST   reviews/
PATCH  reviews/{review_id}/
DELETE reviews/{review_id}/
POST   reviews/{review_id}/like/
POST   reviews/{review_id}/report/
```

التقييم الجديد يكون قيد مراجعة الإدارة، ولكل مستخدم تقييم واحد فقط لكل نشاط. الإعجاب يعمل بالتبديل، ولا يمكن للمستخدم الإعجاب بتقييمه الشخصي.

بيانات البلاغ:

```json
{
  "reason": "سبب البلاغ"
}
```

يسمح ببلاغ واحد فقط من المستخدم نفسه على التقييم.

### المطالبة بالعروض

```text
POST deals/{deal_slug}/claim/
GET  deal-claims/
```

تُنفّذ المطالبة داخل transaction وقفل قاعدة بيانات لمنع تجاوز الحد الكلي للعرض أو حد الاستخدام لكل مستخدم.

## إعدادات التطبيق والتحديثات

```text
GET app-config/?platform=android&version=1.0.0
GET app-config/?platform=ios&version=1.0.0
```

يعيد حالة الصيانة، السماح بالتسجيل والتقييمات، بيانات الدعم، أحدث إصدار، أقل إصدار مسموح، رابط المتجر، وحقلي `update_available` و`update_required`.

## تسجيل أجهزة الموبايل

```text
GET    devices/
POST   devices/
DELETE devices/{device_id}/
```

مثال التسجيل:

```json
{
  "token": "firebase-device-token",
  "platform": "android",
  "device_id": "device-uuid",
  "app_version": "1.0.0",
  "language": "ar"
}
```

عند تغير صاحب Token يتم نقله تلقائيًا إلى المستخدم الحالي، وعند الحذف يصبح الجهاز غير نشط. يمكن إرسال `device_token` مع طلب تسجيل الخروج لتعطيل الجهاز.

## صندوق الإشعارات

```text
GET    notifications/
GET    notifications/unread-count/
POST   notifications/{notification_id}/read/
POST   notifications/read-all/
DELETE notifications/{notification_id}/
```

يدعم المحتوى العربية والإنجليزية، ويمكن تمرير `language=en` أو ترويسة `Accept-Language`.

إرسال المدير:

```text
POST admin/notifications/send/
```

```json
{
  "user_ids": [1, 2],
  "title_ar": "عرض جديد",
  "title_en": "New deal",
  "body_ar": "يوجد عرض جديد بالقرب منك",
  "body_en": "A new deal is available near you",
  "notification_type": "deal",
  "data": {"deal_id": 10}
}
```

يمكن للمدير استخدام `send_to_all: true` بدل `user_ids`.

## إعداد Firebase

صندوق الإشعارات يعمل دون Firebase. لتفعيل Push Notifications اضبط:

```env
PUSH_NOTIFICATIONS_ENABLED=True
FIREBASE_CREDENTIALS_PATH=/secure/path/firebase-service-account.json
```

يجب ألا يُرفع ملف حساب Firebase الخدمي إلى GitHub.

## استجابات الأخطاء

أخطاء DRF القياسية ترجع بالشكل التالي:

```json
{
  "success": false,
  "status_code": 401,
  "message": "تفاصيل الخطأ",
  "errors": {
    "detail": "تفاصيل الخطأ"
  }
}
```

## خطوات النشر

بعد تحديث الكود يجب تشغيل:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py test
```

أمر `migrate` ضروري لإنشاء جداول قائمة JWT السوداء المستخدمة في تسجيل الخروج.
