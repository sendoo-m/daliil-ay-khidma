# 👤 Accounts System

نظام إدارة الحسابات لدليل أي خدمة

## 🎯 Overview

نظام حسابات كامل مع Custom User Model وجميع وظائف المصادقة وإدارة المستخدمين.

---

## ✨ Features

### 🔐 Authentication
- ✅ **التسجيل** - إنشاء حساب جديد
- ✅ **تسجيل الدخول** - دخول آمن
- ✅ **تسجيل الخروج** - خروج من الحساب
- ✅ **استرجاع كلمة المرور** - عبر البريد الإلكتروني

### 👤 Profile Management
- ✅ **الملف الشخصي** - عرض وتحديث
- ✅ **الصورة الشخصية** - رفع وتعديل
- ✅ **تغيير كلمة المرور** - تحديث الأمان

### 📱 Custom User Model
- ✅ **رقم الهاتف** - إلزامي مع تحقق
- ✅ **البريد الإلكتروني** - فريد مع تحقق
- ✅ **نبذة** - Bio شخصية
- ✅ **نوع الحساب** - Owner/Admin/User

---

## 📚 User Model Fields

```python
class User(AbstractUser):
    # الحقول المخصصة
    phone = CharField(unique=True)          # رقم الهاتف المصري
    profile_picture = ImageField()          # الصورة الشخصية
    bio = TextField()                       # نبذة
    city = CharField()                      # المدينة
    
    # الحالة
    email_verified = BooleanField()         # تم التحقق من البريد
    is_business_owner = BooleanField()      # صاحب محل
    
    # التواريخ
    created_at = DateTimeField()            # تاريخ الإنشاء
    updated_at = DateTimeField()            # تاريخ التحديث
```

### 🔑 Properties

```python
user.full_name              # الاسم الكامل
user.has_businesses         # هل لديه محلات
user.total_businesses       # عدد المحلات
user.get_profile_picture_url()  # رابط الصورة
```

---

## 🛣️ URL Structure

```
/accounts/register/                     # التسجيل
/accounts/login/                        # تسجيل الدخول
/accounts/logout/                       # تسجيل الخروج

/accounts/profile/                      # الملف الشخصي

/accounts/password/change/              # تغيير كلمة المرور
/accounts/password/reset/               # استرجاع كلمة المرور
/accounts/password/reset/done/          # تم الإرسال
/accounts/password/reset/<uidb64>/<token>/  # تأكيد الاسترجاع
/accounts/password/reset/complete/      # اكتمل
```

---

## 📝 Forms

### 1️⃣ RegistrationForm
نموذج إنشاء حساب جديد
- Username (unique)
- Email (unique)
- Phone (unique, Egyptian format)
- Password
- Password Confirmation

### 2️⃣ LoginForm
نموذج تسجيل الدخول
- Username/Email
- Password

### 3️⃣ ProfileUpdateForm
نموذج تحديث الملف الشخصي
- First Name
- Last Name
- Email
- Phone
- Profile Picture
- Bio
- City

### 4️⃣ PasswordChangeForm
تغيير كلمة المرور
- Old Password
- New Password
- Confirm New Password

### 5️⃣ PasswordResetForm
استرجاع كلمة المرور
- Email

---

## 🛠️ Setup Instructions

### 1. Update Settings

```python
# config/settings.py or settings/base.py

INSTALLED_APPS = [
    # ...
    'apps.accounts',
    # ...
]

# تحديد Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# التوجيه بعد الدخول/الخروج
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

### 2. Add URLs

```python
# config/urls.py

from django.urls import path, include

urlpatterns = [
    # ...
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    # ...
]
```

### 3. Run Migrations

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 📊 Admin Panel

Django Admin مخصص مع:

### 📋 List Display
- Username
- Email
- Phone
- Full Name
- Profile Picture (thumbnail)
- Account Type (badge)
- Email Status (verified/not)
- Active Status
- Date Joined

### 🔍 Search & Filter
**Search:** Username, Email, Phone, Name  
**Filters:** Account Type, Email Verified, Active, Staff, Superuser, Date Joined

### ⚡ Actions
- تفعيل البريد الإلكتروني
- تحويل لصاحب محل
- تفعيل المستخدمين

---

## 🎯 Usage Examples

### في Views

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    user = request.user
    
    # الوصول للحقول
    print(user.phone)
    print(user.full_name)
    print(user.is_business_owner)
    
    # التحقق من المحلات
    if user.has_businesses:
        businesses = user.businesses.all()
```

### في Templates

```django
{% if user.is_authenticated %}
    <p>مرحباً {{ user.full_name }}</p>
    <img src="{{ user.get_profile_picture_url }}" alt="Profile">
    
    {% if user.is_business_owner %}
        <span>صاحب محل</span>
    {% endif %}
{% endif %}
```

---

## 🔒 Security Features

✅ **Password Validation** - قواعد Django لكلمات المرور  
✅ **Phone Validation** - Egyptian format only (01xxxxxxxxx)  
✅ **Email Uniqueness** - منع التكرار  
✅ **Phone Uniqueness** - منع التكرار  
✅ **CSRF Protection** - محمي في كل النماذج  
✅ **Session Auth** - جلسات آمنة  

---

## 🔧 Future Enhancements

- [ ] Email Verification (2FA)
- [ ] Social Login (Google, Facebook)
- [ ] Phone SMS Verification
- [ ] Profile Completion Progress
- [ ] Activity Logs
- [ ] API Authentication (JWT)

---

## ✅ Testing

```bash
# Run tests
python manage.py test apps.accounts

# Check migrations
python manage.py makemigrations --dry-run
python manage.py migrate --plan
```

---

## 📝 License

Part of Daliil Ay Khidma project
