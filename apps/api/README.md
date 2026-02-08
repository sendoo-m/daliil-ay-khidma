# Daliil Ay Khidma - REST API v2

## 🎯 Overview

Comprehensive REST API for the Daliil Ay Khidma platform with three main interfaces:

1. **Public API** - For mobile app users
2. **Business Owner API** - For business management
3. **Admin API** - For platform administration

## 📁 Project Structure

```
apps/api/
├── serializers/
│   ├── __init__.py
│   ├── admin.py              # Admin serializers
│   ├── business_owner.py     # Business owner serializers
│   ├── deals.py              # Deal serializers (public)
│   ├── directory.py          # Business & Category serializers (public)
│   ├── products.py           # Product serializers (public)
│   ├── reviews.py            # Review serializers (public)
│   └── subscriptions.py      # Subscription serializers
├── views/
│   ├── __init__.py
│   ├── admin.py              # Admin views
│   ├── auth.py               # Authentication views
│   ├── business_owner.py     # Business owner views
│   ├── deals.py              # Deal views (public)
│   ├── directory.py          # Business & Category views (public)
│   ├── products.py           # Product views (public)
│   ├── reviews.py            # Review views (public)
│   └── subscriptions.py      # Subscription views
├── authentication.py         # Custom authentication
├── pagination.py             # Custom pagination
├── permissions.py            # Custom permissions
├── urls.py                   # API v1 URLs (legacy)
├── urls_v2.py               # API v2 URLs (new)
└── README.md                # This file
```

## 🔑 Authentication

### JWT Authentication

#### Register
```http
POST /api/v2/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

#### Login
```http
POST /api/v2/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "SecurePass123!"
}
```

#### Use Token
```http
GET /api/v2/businesses/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 📱 API Endpoints

### Public API

#### Categories
```
GET    /api/v2/categories/
GET    /api/v2/categories/{id}/
```

#### Businesses
```
GET    /api/v2/businesses/
GET    /api/v2/businesses/{id}/
GET    /api/v2/businesses/search/
GET    /api/v2/businesses/nearby/
```

#### Products
```
GET    /api/v2/products/
GET    /api/v2/products/{id}/
```

#### Deals
```
GET    /api/v2/deals/
GET    /api/v2/deals/{id}/
POST   /api/v2/deals/{id}/use/
```

#### Reviews
```
GET    /api/v2/reviews/
POST   /api/v2/reviews/
GET    /api/v2/reviews/{id}/
PUT    /api/v2/reviews/{id}/
DELETE /api/v2/reviews/{id}/
```

### Business Owner API

#### Dashboard
```
GET /api/v2/business-owner/dashboard/stats/
```

#### Businesses
```
GET    /api/v2/business-owner/businesses/
POST   /api/v2/business-owner/businesses/
GET    /api/v2/business-owner/businesses/{id}/
PUT    /api/v2/business-owner/businesses/{id}/
DELETE /api/v2/business-owner/businesses/{id}/
```

#### Products (nested under business)
```
GET    /api/v2/business-owner/businesses/{id}/products/
POST   /api/v2/business-owner/businesses/{id}/products/
GET    /api/v2/business-owner/businesses/{id}/products/{pid}/
PUT    /api/v2/business-owner/businesses/{id}/products/{pid}/
DELETE /api/v2/business-owner/businesses/{id}/products/{pid}/
```

#### Deals (nested under business)
```
GET    /api/v2/business-owner/businesses/{id}/deals/
POST   /api/v2/business-owner/businesses/{id}/deals/
GET    /api/v2/business-owner/businesses/{id}/deals/{did}/
PUT    /api/v2/business-owner/businesses/{id}/deals/{did}/
DELETE /api/v2/business-owner/businesses/{id}/deals/{did}/
```

#### Reviews (read-only, nested under business)
```
GET /api/v2/business-owner/businesses/{id}/reviews/
```

### Admin API

#### Dashboard
```
GET /api/v2/admin/dashboard/stats/
GET /api/v2/admin/dashboard/analytics/
```

#### Users
```
GET    /api/v2/admin/users/
GET    /api/v2/admin/users/{id}/
PUT    /api/v2/admin/users/{id}/
DELETE /api/v2/admin/users/{id}/
POST   /api/v2/admin/users/{id}/toggle_active/
POST   /api/v2/admin/users/{id}/make_staff/
```

#### Businesses
```
GET    /api/v2/admin/businesses/
GET    /api/v2/admin/businesses/{id}/
PUT    /api/v2/admin/businesses/{id}/
DELETE /api/v2/admin/businesses/{id}/
POST   /api/v2/admin/businesses/{id}/verify/
POST   /api/v2/admin/businesses/{id}/toggle_featured/
```

#### Categories
```
GET    /api/v2/admin/categories/
POST   /api/v2/admin/categories/
GET    /api/v2/admin/categories/{id}/
PUT    /api/v2/admin/categories/{id}/
DELETE /api/v2/admin/categories/{id}/
```

#### Products
```
GET    /api/v2/admin/products/
GET    /api/v2/admin/products/{id}/
PUT    /api/v2/admin/products/{id}/
DELETE /api/v2/admin/products/{id}/
```

#### Deals
```
GET    /api/v2/admin/deals/
GET    /api/v2/admin/deals/{id}/
PUT    /api/v2/admin/deals/{id}/
DELETE /api/v2/admin/deals/{id}/
```

#### Reviews
```
GET    /api/v2/admin/reviews/
GET    /api/v2/admin/reviews/{id}/
PUT    /api/v2/admin/reviews/{id}/
DELETE /api/v2/admin/reviews/{id}/
POST   /api/v2/admin/reviews/{id}/approve/
POST   /api/v2/admin/reviews/{id}/reject/
```

## 🔒 Permissions

### Custom Permission Classes

- `IsAdminUser` - Only admin/staff users
- `IsBusinessOwner` - Only business owners
- `IsOwnerOrReadOnly` - Owner can edit, others read-only
- `IsAdminOrReadOnly` - Admin can edit, others read-only

## 📄 Pagination

All list endpoints support pagination:

```
GET /api/v2/businesses/?page=1&page_size=20
```

Response:
```json
{
  "count": 150,
  "next": "http://api.example.com/api/v2/businesses/?page=2",
  "previous": null,
  "results": [...]
}
```

## 🔍 Filtering & Search

Most endpoints support filtering:

```
GET /api/v2/businesses/?search=restaurant&category=1&is_verified=true&ordering=-created_at
```

## 🛠️ Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Server
```bash
python manage.py runserver 0.0.0.0:8008
```

### Test API
```bash
# Get categories
curl http://localhost:8008/api/v2/categories/

# Register user
curl -X POST http://localhost:8008/api/v2/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"Test123!","password_confirm":"Test123!"}'

# Login
curl -X POST http://localhost:8008/api/v2/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!"}'
```

## 📚 Complete Documentation

See [API_DOCUMENTATION.md](../../API_DOCUMENTATION.md) in the project root for complete API documentation with examples.

## 🐛 Error Handling

### Error Response Format
```json
{
  "error": "Error message",
  "detail": "Additional details"
}
```

### HTTP Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## 📱 Mobile App Integration

### Flutter
See example in [API_DOCUMENTATION.md](../../API_DOCUMENTATION.md#-mobile-app-integration)

### React Native
See example in [API_DOCUMENTATION.md](../../API_DOCUMENTATION.md#-mobile-app-integration)

## 🔗 Useful Links

- **API Root:** http://localhost:8008/api/v2/
- **Admin Panel:** http://localhost:8008/admin/
- **Dashboard:** http://localhost:8008/admin-dashboard/

## 📝 Notes

1. All dates in ISO 8601 format: `YYYY-MM-DD`
2. All datetimes in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
3. Image uploads use multipart/form-data
4. Max file size: 5MB
5. Supported formats: JPG, PNG, WebP

## 🤝 Contributing

For bugs or feature requests, please create an issue on GitHub.

---

**Version:** 2.0  
**Last Updated:** February 2026
