# دليل أي خدمة (Daliil Ay Khidma)

## 📋 نظرة عامة
**دليل أي خدمة** هو نظام دليل خدمات شامل ومتطور تم بناؤه باستخدام Django، يجمع أفضل المميزات من نظامين سابقين لإنشاء منصة قوية واحترافية.

## 🚀 المميزات الرئيسية
- نظام إدارة خدمات متقدم
- تصنيفات وتصنيفات فرعية
- نظام تقييمات ومراجعات
- بحث متقدم وفلترة
- لوحة تحكم احترافية
- دعم كامل للغة العربية
- تصميم responsive

## 🛠️ التقنيات المستخدمة
- **Backend**: Django 5.1.5
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5 + jQuery
- **Python**: 3.13.7

## 📦 التثبيت

### المتطلبات
- Python 3.13.7
- PostgreSQL (للإنتاج) أو SQLite (للتطوير)

### خطوات التثبيت

1. **Clone المشروع**
```bash
git clone https://github.com/sendoo-m/daliil-ay-khidma.git
cd daliil-ay-khidma
```

2. **إنشاء البيئة الافتراضية**
```bash
python -m venv venv
source venv/bin/activate  # في Linux/Mac
venv\Scripts\activate     # في Windows
```

3. **تثبيت المكتبات**
```bash
pip install -r requirements.txt
```

4. **إعداد البيئة**
```bash
cp .env.example .env
# قم بتعديل ملف .env بالإعدادات المناسبة
```

5. **تشغيل Migrations**
```bash
python manage.py migrate
```

6. **إنشاء superuser**
```bash
python manage.py createsuperuser
```

7. **تشغيل السيرفر**
```bash
python manage.py runserver
```

## 📁 هيكل المشروع
```
daliil-ay-khidma/
├── config/              # إعدادات المشروع
├── apps/                # تطبيقات Django
│   ├── core/           # الوظائف الأساسية
│   ├── accounts/       # إدارة المستخدمين
│   ├── services/       # الخدمات
│   ├── categories/     # التصنيفات
│   ├── reviews/        # التقييمات
│   ├── search/         # البحث
│   └── dashboard/      # لوحة التحكم
├── static/             # الملفات الثابتة
├── media/              # ملفات المستخدمين
├── templates/          # القوالب
└── locale/             # الترجمات
```

## 👨‍💻 المطور
**Sendoo M.**

## 📝 الترخيص
هذا المشروع خاص ومملوك لـ Sendoo M.

## 🤝 المساهمة
هذا مشروع خاص، للاستفسارات يرجى التواصل مع المطور.

---

**نسخة**: 1.0.0 (قيد التطوير)
**تاريخ البدء**: يناير 2026
