# 🔌 Daliil Ay Khidma REST API

مستندات كاملة لـ REST API

## 🎯 Base URL

```
http://localhost:8000/api/v1/
```

## 🔑 Authentication

يدعم الـ API طريقتين للمصادقة:

1. **Session Authentication** - للتطبيقات الويب
2. **Basic Authentication** - للتطبيقات الخارجية

## 📚 Endpoints

### 🏛️ Directory (Locations)

#### Governorates (المحافظات)

```http
GET    /api/v1/governorates/           # List all governorates
GET    /api/v1/governorates/{slug}/    # Get governorate details
```

**Example Response:**
```json
{
  "id": 1,
  "name_en": "Cairo",
  "name_ar": "القاهرة",
  "slug": "cairo",
  "is_active": true
}
```

---

#### Cities (المدن)

```http
GET    /api/v1/cities/                 # List all cities
GET    /api/v1/cities/{slug}/          # Get city details
```

**Query Parameters:**
- `governorate` - Filter by governorate ID

---

#### Districts (الأحياء)

```http
GET    /api/v1/districts/              # List all districts
GET    /api/v1/districts/{slug}/       # Get district details
```

**Query Parameters:**
- `city` - Filter by city ID
- `city__governorate` - Filter by governorate ID

---

### 🏪 Businesses (المحال التجارية)

```http
GET    /api/v1/businesses/                    # List all businesses
GET    /api/v1/businesses/featured/           # Featured businesses
GET    /api/v1/businesses/shops/              # المحلات التجارية (Shop type only)
GET    /api/v1/businesses/crafts/             # الحرف والخدمات (Craft/Trade services)
GET    /api/v1/businesses/public_services/    # الخدمات العامة (Public services)
GET    /api/v1/businesses/my_businesses/      # My businesses (Auth required)
GET    /api/v1/businesses/{slug}/             # Business details
POST   /api/v1/businesses/                    # Create business (Auth required)
PUT    /api/v1/businesses/{slug}/             # Update business (Owner only)
DELETE /api/v1/businesses/{slug}/             # Delete business (Owner only)
POST   /api/v1/businesses/{slug}/increment_view/   # Increment view count
POST   /api/v1/businesses/{slug}/increment_click/  # Increment click count
```

**Query Parameters:**
- `business_type` - Filter by type (`shop`, `craft`, `public`) ⭐ NEW
- `category` - Filter by category ID
- `district` - Filter by district ID
- `is_verified` - Filter verified businesses
- `is_featured` - Filter featured businesses
- `search` - Search in name/description
- `ordering` - Order by field (e.g., `-created_at`, `view_count`)

**Business Types (أنواع المحال):**
- `shop` - 🏪 محل تجاري (Commercial shop with products)
- `craft` - 🔧 حرفة أو خدمة حرفية (Plumber, electrician, carpenter, etc.)
- `public` - 🏛️ خدمة عامة (Public hospital, fire station, public park, etc.)

**Example Response:**
```json
{
  "id": 1,
  "name_en": "Tech Store",
  "name_ar": "متجر التكنولوجيا",
  "slug": "tech-store",
  "business_type": "shop",
  "business_type_display": "محل تجاري / Commercial Shop",
  "business_type_icon": "🏪",
  "is_shop": true,
  "is_craft": false,
  "is_public_service": false,
  "category": {...},
  "district": {...},
  "phone": "+20123456789",
  "average_rating": 4.5,
  "total_reviews": 25,
  "is_verified": true,
  "is_featured": false
}
```

**Usage Examples:**
```bash
# Get all commercial shops
curl "http://localhost:8000/api/v1/businesses/?business_type=shop"

# Get all crafts/trade services (plumber, electrician, etc.)
curl "http://localhost:8000/api/v1/businesses/?business_type=craft"

# Get all public services (hospitals, fire stations, etc.)
curl "http://localhost:8000/api/v1/businesses/?business_type=public"

# Using custom endpoints
curl "http://localhost:8000/api/v1/businesses/shops/"
curl "http://localhost:8000/api/v1/businesses/crafts/"
curl "http://localhost:8000/api/v1/businesses/public_services/"
```

---

### 📦 Products (المنتجات)

```http
GET    /api/v1/products/                      # List all products
GET    /api/v1/products/featured/             # Featured products
GET    /api/v1/products/on_sale/              # Products on sale
GET    /api/v1/products/{slug}/               # Product details
POST   /api/v1/products/                      # Create product (Auth required)
PUT    /api/v1/products/{slug}/               # Update product (Owner only)
DELETE /api/v1/products/{slug}/               # Delete product (Owner only)
POST   /api/v1/products/{slug}/increment_view/ # Increment view count
```

**Query Parameters:**
- `product_type` - Filter by type (`product` or `service`)
- `business` - Filter by business ID
- `is_available` - Filter available products
- `is_featured` - Filter featured products
- `search` - Search in name/description
- `ordering` - Order by field (e.g., `price`, `-view_count`)

**Example Response:**
```json
{
  "id": 1,
  "name_en": "Laptop",
  "name_ar": "حاسوب محمول",
  "slug": "laptop",
  "product_type": "product",
  "price": 15000.00,
  "old_price": 18000.00,
  "discount_percentage": 16.67,
  "has_discount": true,
  "is_available": true,
  "business": {...},
  "primary_image": {...}
}
```

---

### 🎁 Deals (العروض)

```http
GET    /api/v1/deals/                         # List active deals
GET    /api/v1/deals/featured/                # Featured deals
GET    /api/v1/deals/ending_soon/             # Deals ending soon
GET    /api/v1/deals/{slug}/                  # Deal details
POST   /api/v1/deals/                         # Create deal (Auth required)
PUT    /api/v1/deals/{slug}/                  # Update deal (Owner only)
DELETE /api/v1/deals/{slug}/                  # Delete deal (Owner only)
POST   /api/v1/deals/{slug}/claim/            # Claim deal (Auth required)
POST   /api/v1/deals/{slug}/increment_view/   # Increment view count
```

**Query Parameters:**
- `deal_type` - Filter by type (`percentage`, `fixed`, `bogo`, `bundle`, `special`)
- `business` - Filter by business ID
- `is_featured` - Filter featured deals
- `search` - Search in title/description

**Example Response:**
```json
{
  "id": 1,
  "title_en": "50% Off",
  "title_ar": "خصم 50%",
  "slug": "50-off",
  "deal_type": "percentage",
  "discount_percentage": 50,
  "original_price": 1000.00,
  "final_price": 500.00,
  "start_date": "2026-01-01T00:00:00",
  "end_date": "2026-02-01T00:00:00",
  "days_remaining": 3,
  "is_valid": true,
  "business": {...}
}
```

---

### 💳 Subscriptions (الاشتراكات)

```http
GET    /api/v1/subscription-plans/            # List all plans
GET    /api/v1/subscription-plans/{id}/       # Plan details
GET    /api/v1/subscription-plans/{id}/pricing/ # Get pricing for all durations

GET    /api/v1/subscriptions/                 # My subscriptions (Auth required)
GET    /api/v1/subscriptions/my_subscription/ # Current active subscription
```

**Example Response:**
```json
{
  "id": 2,
  "name": "basic",
  "display_name_en": "Basic Plan",
  "display_name_ar": "خطة أساسية",
  "price_monthly": 50.00,
  "price_annual": 500.00,
  "max_products": 50,
  "can_upload_images": true,
  "can_show_prices": true
}
```

---

### ⭐ Favorites (المفضلة)

```http
GET    /api/v1/favorites/                     # My favorites (Auth required)
POST   /api/v1/favorites/                     # Add to favorites
DELETE /api/v1/favorites/{id}/                # Remove from favorites
POST   /api/v1/favorites/toggle/              # Toggle favorite status
```

**Toggle Request:**
```json
{
  "business_id": 123
}
```

**Toggle Response:**
```json
{
  "status": "added",
  "is_favorite": true
}
```

---

### 🏷️ Categories (الفئات)

```http
GET    /api/v1/categories/                    # List all categories
GET    /api/v1/categories/{slug}/             # Category details
```

---

## 📊 Pagination

جميع القوائم مقسمة لصفحات:

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Results per page (default: 20, max: 100)

**Response Format:**
```json
{
  "count": 150,
  "next": "http://api.example.com/api/v1/businesses/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 🔍 Filtering & Search

**Search:**
```http
GET /api/v1/businesses/?search=tech
```

**Filtering:**
```http
GET /api/v1/businesses/?category=1&is_verified=true
GET /api/v1/businesses/?business_type=craft&district=5
```

**Ordering:**
```http
GET /api/v1/businesses/?ordering=-created_at
GET /api/v1/products/?ordering=price,-view_count
```

**Combined:**
```http
GET /api/v1/businesses/?business_type=shop&category=1&search=shop&ordering=-view_count&page=2
```

---

## 🚫 Error Responses

**400 Bad Request:**
```json
{
  "field_name": ["This field is required."]
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

---

## 🛠️ Development Tools

### Browsable API

زر الرابط في المتصفح:
```
http://localhost:8000/api/v1/
```

### API Documentation

للحصول على التوثيق الكامل:
```
http://localhost:8000/api/v1/docs/
```

---

## 📝 Example Usage

### Python (requests)

```python
import requests

# Get all businesses
response = requests.get('http://localhost:8000/api/v1/businesses/')
data = response.json()

# Get all craft services (plumber, electrician, etc.)
response = requests.get('http://localhost:8000/api/v1/businesses/crafts/')
crafts = response.json()

# Get business details
response = requests.get('http://localhost:8000/api/v1/businesses/tech-store/')
business = response.json()

# Create business (with authentication)
session = requests.Session()
session.auth = ('username', 'password')

business_data = {
    'name_en': 'Ahmed the Plumber',
    'name_ar': 'أحمد السباك',
    'business_type': 'craft',  # NEW
    'category': 15,
    'district': 5,
    'phone': '01234567890'
}

response = session.post(
    'http://localhost:8000/api/v1/businesses/',
    json=business_data
)
```

### JavaScript (fetch)

```javascript
// Get all public services
fetch('http://localhost:8000/api/v1/businesses/public_services/')
  .then(response => response.json())
  .then(data => console.log(data));

// Filter by business type
fetch('http://localhost:8000/api/v1/businesses/?business_type=shop&category=1')
  .then(response => response.json())
  .then(data => console.log(data));

// Create craft service business
fetch('http://localhost:8000/api/v1/businesses/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  credentials: 'include',
  body: JSON.stringify({
    name_en: 'Ali the Electrician',
    name_ar: 'علي الكهربائي',
    business_type: 'craft',
    category: 16,
    district: 3,
    phone: '01098765432'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL

```bash
# Get all businesses
curl http://localhost:8000/api/v1/businesses/

# Get all craft services
curl http://localhost:8000/api/v1/businesses/crafts/

# Filter by business type
curl "http://localhost:8000/api/v1/businesses/?business_type=public"

# Search craft services
curl "http://localhost:8000/api/v1/businesses/?business_type=craft&search=سباك"

# Create public service (with auth)
curl -X POST http://localhost:8000/api/v1/businesses/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "name_en": "City Hospital",
    "name_ar": "مستشفى المدينة",
    "business_type": "public",
    "category": 20,
    "district": 1,
    "phone": "0123456789"
  }'
```

---

## ✅ Best Practices

1. **استخدم Pagination** - لا تحمل كل البيانات مرة واحدة
2. **فلتر البيانات** - استخدم query parameters للحصول على ما تحتاجه فقط
3. **احفظ البيانات** - Cache responses لتقليل عدد الطلبات
4. **استخدم HTTPS** - دائماً في الإنتاج
5. **معالجة الأخطاء** - تعامل مع جميع رموز الأخطاء
6. **استخدم business_type** - استخدم الفلتر الجديد لتحسين تجربة المستخدم

---

## 🔒 Rate Limiting

لم يتم تفعيل rate limiting بعد، لكن يُنصح بعدم إرسال أكثر من 100 طلب في الدقيقة.

---

## 👨‍💻 Support

للمساعدة أو الإبلاغ عن مشاكل:
- Email: support@daliil-ay-khidma.com
- GitHub: https://github.com/sendoo-m/daliil-ay-khidma
