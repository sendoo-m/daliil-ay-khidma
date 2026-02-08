# 🚀 Daliil Ay Khidma - API Documentation v2

## 🎯 Overview

This is the comprehensive REST API for the Daliil Ay Khidma platform. The API provides three main interfaces:

1. **Public API** - For mobile app users (browsing, searching, reviews)
2. **Business Owner API** - For business owners to manage their businesses
3. **Admin API** - For platform administrators

## 🔑 Authentication

### JWT Authentication

The API uses JWT (JSON Web Tokens) for authentication.

#### Register New User
```http
POST /api/v2/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "Test",
  "last_name": "User"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
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

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "is_staff": false,
    "is_superuser": false
  }
}
```

#### Refresh Token
```http
POST /api/v2/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get User Profile
```http
GET /api/v2/auth/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Update Profile
```http
PUT /api/v2/auth/profile/update/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Name",
  "email": "newemail@example.com"
}
```

#### Change Password
```http
POST /api/v2/auth/change-password/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "old_password": "OldPass123!",
  "new_password": "NewPass123!",
  "new_password_confirm": "NewPass123!"
}
```

---

## 👥 Public API (Mobile App Users)

### Categories

#### List Categories
```http
GET /api/v2/categories/
```

**Query Parameters:**
- `is_active` - Filter by active status (true/false)
- `parent` - Filter by parent category ID
- `search` - Search in name
- `ordering` - Sort by field (order, name_ar, name_en)

#### Get Category Detail
```http
GET /api/v2/categories/{id}/
```

### Businesses

#### List Businesses
```http
GET /api/v2/businesses/
```

**Query Parameters:**
- `category` - Filter by category ID
- `is_verified` - Filter by verification status
- `is_featured` - Filter by featured status
- `business_type` - Filter by type (storefront, online, service, hybrid)
- `city` - Filter by city
- `search` - Search in name, description
- `ordering` - Sort by field (created_at, views_count, -rating)

#### Get Business Detail
```http
GET /api/v2/businesses/{id}/
```

**Response includes:**
- Full business details
- Products
- Active deals
- Reviews
- Average rating

#### Search Businesses
```http
GET /api/v2/businesses/search/?q=restaurant
```

#### Nearby Businesses
```http
GET /api/v2/businesses/nearby/?lat=24.7136&lon=46.6753&radius=5
```

### Products

#### List Products
```http
GET /api/v2/products/
```

**Query Parameters:**
- `business` - Filter by business ID
- `product_type` - Filter by type (product, service)
- `is_available` - Filter by availability
- `is_featured` - Filter by featured status
- `min_price` - Minimum price
- `max_price` - Maximum price
- `search` - Search in name, description
- `ordering` - Sort by field (created_at, price, -price)

#### Get Product Detail
```http
GET /api/v2/products/{id}/
```

### Deals

#### List Deals
```http
GET /api/v2/deals/
```

**Query Parameters:**
- `business` - Filter by business ID
- `deal_type` - Filter by type (percentage, fixed, buy_one_get_one)
- `is_featured` - Filter by featured status
- `is_active` - Show only active deals
- `search` - Search in title, description
- `ordering` - Sort by field (created_at, -discount_percentage)

#### Get Deal Detail
```http
GET /api/v2/deals/{id}/
```

#### Use Deal (Track Usage)
```http
POST /api/v2/deals/{id}/use/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Reviews

#### List Reviews
```http
GET /api/v2/reviews/
```

**Query Parameters:**
- `business` - Filter by business ID
- `rating` - Filter by rating (1-5)
- `is_approved` - Filter by approval status
- `ordering` - Sort by field (created_at, rating)

#### Create Review
```http
POST /api/v2/reviews/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "business": 1,
  "rating": 5,
  "comment": "Great service and quality!"
}
```

#### Update Review
```http
PUT /api/v2/reviews/{id}/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "rating": 4,
  "comment": "Updated review"
}
```

#### Delete Review
```http
DELETE /api/v2/reviews/{id}/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 🏢 Business Owner API

**Note:** All endpoints require authentication and user must be the business owner.

### Dashboard

#### Get Stats
```http
GET /api/v2/business-owner/dashboard/stats/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "total_businesses": 3,
  "verified_businesses": 2,
  "total_products": 25,
  "total_deals": 5,
  "active_deals": 3,
  "total_reviews": 45,
  "average_rating": 4.5,
  "total_views": 1250,
  "total_clicks": 320
}
```

### Manage Businesses

#### List My Businesses
```http
GET /api/v2/business-owner/businesses/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Create Business
```http
POST /api/v2/business-owner/businesses/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: multipart/form-data

{
  "name_ar": "مطعم الفخامة",
  "name_en": "Al Fakhama Restaurant",
  "category": 1,
  "business_type": "storefront",
  "description_ar": "...",
  "description_en": "...",
  "phone": "+966501234567",
  "email": "info@alfakhama.com",
  "address_ar": "...",
  "city_ar": "الرياض",
  "logo": <file>
}
```

#### Update Business
```http
PUT /api/v2/business-owner/businesses/{id}/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Delete Business
```http
DELETE /api/v2/business-owner/businesses/{id}/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Manage Products

#### List Business Products
```http
GET /api/v2/business-owner/businesses/{business_id}/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Create Product
```http
POST /api/v2/business-owner/businesses/{business_id}/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: multipart/form-data

{
  "name_ar": "برجر فاخر",
  "name_en": "Premium Burger",
  "product_type": "product",
  "description_ar": "...",
  "price": 35.00,
  "is_available": true,
  "image": <file>
}
```

#### Update Product
```http
PUT /api/v2/business-owner/businesses/{business_id}/products/{id}/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Delete Product
```http
DELETE /api/v2/business-owner/businesses/{business_id}/products/{id}/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Manage Deals

#### List Business Deals
```http
GET /api/v2/business-owner/businesses/{business_id}/deals/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Create Deal
```http
POST /api/v2/business-owner/businesses/{business_id}/deals/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "title_ar": "خصم 50%",
  "title_en": "50% Off",
  "deal_type": "percentage",
  "discount_percentage": 50,
  "start_date": "2026-02-01",
  "end_date": "2026-02-28",
  "is_active": true
}
```

### View Reviews

#### List Business Reviews
```http
GET /api/v2/business-owner/businesses/{business_id}/reviews/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 🔒 Admin API

**Note:** All endpoints require admin/staff authentication.

### Dashboard

#### Get Dashboard Stats
```http
GET /api/v2/admin/dashboard/stats/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "total_users": 1250,
  "active_users": 1100,
  "new_users_week": 45,
  "staff_users": 5,
  "total_businesses": 320,
  "verified_businesses": 280,
  "pending_verification": 40,
  "featured_businesses": 25,
  "total_products": 1580,
  "active_products": 1420,
  "total_deals": 125,
  "active_deals": 85,
  "total_reviews": 2450,
  "pending_reviews": 32,
  "average_rating": 4.3,
  "total_views": 125000,
  "total_clicks": 35000
}
```

#### Get Analytics
```http
GET /api/v2/admin/dashboard/analytics/?period=monthly
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### User Management

#### List Users
```http
GET /api/v2/admin/users/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Query Parameters:**
- `is_active` - Filter by active status
- `is_staff` - Filter by staff status
- `is_superuser` - Filter by superuser status
- `search` - Search in username, email, name
- `ordering` - Sort by field

#### Get User Detail
```http
GET /api/v2/admin/users/{id}/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Toggle User Active Status
```http
POST /api/v2/admin/users/{id}/toggle_active/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Make User Staff
```http
POST /api/v2/admin/users/{id}/make_staff/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Business Management

#### List All Businesses
```http
GET /api/v2/admin/businesses/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Verify Business
```http
POST /api/v2/admin/businesses/{id}/verify/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Toggle Featured
```http
POST /api/v2/admin/businesses/{id}/toggle_featured/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Category Management

#### List Categories
```http
GET /api/v2/admin/categories/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Create Category
```http
POST /api/v2/admin/categories/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: multipart/form-data

{
  "name_ar": "مطاعم",
  "name_en": "Restaurants",
  "icon": <file>,
  "is_active": true,
  "order": 1
}
```

### Review Management

#### List All Reviews
```http
GET /api/v2/admin/reviews/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Approve Review
```http
POST /api/v2/admin/reviews/{id}/approve/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Reject Review
```http
POST /api/v2/admin/reviews/{id}/reject/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📊 Pagination

All list endpoints support pagination:

```http
GET /api/v2/businesses/?page=2&page_size=20
```

**Response:**
```json
{
  "count": 150,
  "next": "http://api.example.com/api/v2/businesses/?page=3",
  "previous": "http://api.example.com/api/v2/businesses/?page=1",
  "results": [...]
}
```

---

## 🔍 Filtering & Searching

Most endpoints support filtering and searching:

```http
GET /api/v2/businesses/?search=restaurant&category=1&is_verified=true&ordering=-created_at
```

---

## ⚠️ Error Handling

### Error Response Format
```json
{
  "error": "Error message here",
  "detail": "Additional details"
}
```

### Common HTTP Status Codes
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 👨‍💻 Development Setup

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
curl http://localhost:8008/api/v2/categories/
```

---

## 📦 Postman Collection

Import the Postman collection for easy testing:

1. Download [Postman Collection](postman_collection.json)
2. Import into Postman
3. Set environment variables:
   - `base_url`: http://localhost:8008
   - `access_token`: Your JWT access token

---

## 📱 Mobile App Integration

### Flutter Example
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://your-domain.com/api/v2';
  String? accessToken;
  
  Future<void> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      accessToken = data['access'];
    }
  }
  
  Future<List<dynamic>> getBusinesses() async {
    final response = await http.get(
      Uri.parse('$baseUrl/businesses/'),
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['results'];
    }
    return [];
  }
}
```

### React Native Example
```javascript
import axios from 'axios';

const API_URL = 'http://your-domain.com/api/v2';
let accessToken = null;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

export const login = async (username, password) => {
  const response = await api.post('/auth/login/', {
    username,
    password,
  });
  accessToken = response.data.access;
  return response.data;
};

export const getBusinesses = async () => {
  const response = await api.get('/businesses/');
  return response.data.results;
};
```

---

## 🔗 Base URLs

- **Development:** http://localhost:8008/api/v2/
- **Production:** https://your-domain.com/api/v2/

---

## 📝 Notes

1. All dates are in ISO 8601 format: `YYYY-MM-DD`
2. All datetimes are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
3. All image uploads should be multipart/form-data
4. Maximum file size: 5MB
5. Supported image formats: JPG, PNG, WebP
6. Rate limiting: 1000 requests/hour per user

---

## ❓ Support

For questions or issues:
- Email: support@daliil-ay-khidma.com
- GitHub Issues: [Create Issue](https://github.com/sendoo-m/daliil-ay-khidma/issues)

---

**Version:** 2.0  
**Last Updated:** February 2026  
**Maintained by:** Daliil Ay Khidma Team
