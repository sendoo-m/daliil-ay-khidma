# Mobile API v2

القاعدة الأساسية لكل نقاط الموبايل:

```text
/api/v2/
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
