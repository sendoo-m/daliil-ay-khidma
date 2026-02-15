# 🛠️ APIs المطلوب تطويرها - Daliil Ay Khidma

## 🏁 الحالة العامة

✅ **جاهز:** 60% من APIs موجودة وتعمل  
⚠️ **مطلوب:** 40% من APIs تحتاج تطوير  
📅 **الوقت المقدر:** 2 أسبوع عمل

---

## 🔴 High Priority - ضروري لتطبيق المستخدم

### 1️⃣ Reviews API - إكمال وتحسين

**الملف:** `apps/api/views/reviews.py`  
**الأولوية:** 🔴 عالية  
**الوقت:** 1 يوم

#### ✅ الموجود حالياً:
```python
class ReviewViewSet(viewsets.ModelViewSet):
    # GET /api/v1/reviews/?business={id}
    queryset = Review.objects.all()
```

#### ❌ المطلوب إضافته:

```python
# 1. Create Review
POST /api/v1/reviews/
{
  "business": 1,
  "rating": 5,
  "comment": "محل رائع وخدمة ممتازة"
}
Permission: IsAuthenticated

# 2. Update Review
PUT /api/v1/reviews/{id}/
{
  "rating": 4,
  "comment": "محدث"
}
Permission: IsOwner (user owns the review)

# 3. Delete Review  
DELETE /api/v1/reviews/{id}/
Permission: IsOwnerOrAdmin

# 4. Business Owner Reply
POST /api/v1/reviews/{id}/reply/
{
  "reply": "شكراً على تقييمك!"
}
Permission: IsBusinessOwner
```

**Implementation Steps:**
```python
# apps/api/views/reviews.py

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user', 'business')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Check if user already reviewed this business
        business = serializer.validated_data['business']
        if Review.objects.filter(
            user=self.request.user, 
            business=business
        ).exists():
            raise ValidationError("You already reviewed this business")
        
        serializer.save(user=self.request.user)
        
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [AllowAny()]
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Business owner reply to review"""
        review = self.get_object()
        
        # Check if user owns the business
        if review.business.owner != request.user:
            return Response(
                {'error': 'You can only reply to reviews of your businesses'},
                status=403
            )
        
        review.owner_reply = request.data.get('reply')
        review.reply_date = timezone.now()
        review.save()
        
        return Response(self.get_serializer(review).data)
```

---

### 2️⃣ Advanced Search API

**الملف:** `apps/api/views/search.py` (جديد)  
**الأولوية:** 🔴 عالية  
**الوقت:** 1 يوم

#### ❌ المطلوب:

```python
# Unified Search Endpoint
GET /api/v1/search/

Query Parameters:
  - q: البحث النصي (required)
  - type: business,product,deal,service (optional)
  - category: category_id (optional)
  - city: city_name (optional)
  - min_rating: 1-5 (optional)
  - sort: relevance,rating,views,created (default: relevance)
  - page_size: 10-100 (default: 20)
  - page: page number

Response:
{
  "count": 150,
  "next": "...",
  "previous": null,
  "results": [
    {
      "type": "business",
      "id": 1,
      "name": "...",
      "description": "...",
      "image": "...",
      "rating": 4.5,
      "relevance_score": 0.95
    },
    ...
  ]
}
```

**Implementation:**
```python
# apps/api/views/search.py

from django.db.models import Q, F, Value, FloatField
from django.db.models.functions import Greatest
from rest_framework.views import APIView
from rest_framework.response import Response

class UnifiedSearchView(APIView):
    """
    Unified search across businesses, products, deals, and services
    """
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({'error': 'Search query required'}, status=400)
        
        search_type = request.GET.get('type', 'all')
        category = request.GET.get('category')
        city = request.GET.get('city')
        min_rating = request.GET.get('min_rating')
        sort = request.GET.get('sort', 'relevance')
        
        results = []
        
        # Search businesses
        if search_type in ['all', 'business', 'service']:
            businesses = self._search_businesses(
                query, category, city, min_rating, search_type
            )
            results.extend(businesses)
        
        # Search products
        if search_type in ['all', 'product']:
            products = self._search_products(query, category)
            results.extend(products)
        
        # Search deals
        if search_type in ['all', 'deal']:
            deals = self._search_deals(query)
            results.extend(deals)
        
        # Sort results
        results = self._sort_results(results, sort)
        
        # Pagination
        page_size = min(int(request.GET.get('page_size', 20)), 100)
        page = int(request.GET.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        return Response({
            'count': len(results),
            'results': results[start:end]
        })
    
    def _search_businesses(self, query, category, city, min_rating, search_type):
        from apps.directory.models import Business
        from apps.api.serializers.directory import BusinessListSerializer
        
        qs = Business.objects.filter(
            Q(name_ar__icontains=query) |
            Q(name_en__icontains=query) |
            Q(description_ar__icontains=query) |
            Q(description_en__icontains=query)
        )
        
        if search_type == 'service':
            qs = qs.filter(type='service')
        elif search_type == 'business':
            qs = qs.filter(type='business')
        
        if category:
            qs = qs.filter(category_id=category)
        
        if city:
            qs = qs.filter(Q(city__name_ar=city) | Q(city__name_en=city))
        
        if min_rating:
            qs = qs.filter(average_rating__gte=float(min_rating))
        
        # Calculate relevance score
        qs = qs.annotate(
            relevance_score=Case(
                When(name_ar__iexact=query, then=Value(1.0)),
                When(name_en__iexact=query, then=Value(1.0)),
                When(name_ar__istartswith=query, then=Value(0.8)),
                When(name_en__istartswith=query, then=Value(0.8)),
                default=Value(0.5),
                output_field=FloatField()
            )
        )
        
        results = []
        for business in qs[:50]:  # Limit to avoid performance issues
            data = BusinessListSerializer(business).data
            data['type'] = 'business' if business.type == 'business' else 'service'
            data['relevance_score'] = business.relevance_score
            results.append(data)
        
        return results
```

---

### 3️⃣ Nearby Businesses API

**الملف:** `apps/api/views/directory.py`  
**الأولوية:** 🔴 عالية  
**الوقت:** 0.5 يوم

#### ❌ المطلوب:

```python
# Get nearby businesses
GET /api/v1/businesses/nearby/

Query Parameters:
  - lat: latitude (required)
  - lng: longitude (required)
  - radius: radius in km (default: 5, max: 50)
  - category: category_id (optional)
  - limit: max results (default: 20, max: 100)

Response:
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "name": "...",
      "distance": 1.5,  // km
      "latitude": 30.0444,
      "longitude": 31.2357,
      ...
    }
  ]
}
```

**Implementation:**
```python
# apps/api/views/directory.py

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import action

class BusinessViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """
        Get businesses near a location
        """
        try:
            lat = float(request.GET.get('lat'))
            lng = float(request.GET.get('lng'))
        except (TypeError, ValueError):
            return Response(
                {'error': 'Valid lat and lng required'}, 
                status=400
            )
        
        radius = float(request.GET.get('radius', 5))  # km
        radius = min(radius, 50)  # max 50km
        
        category = request.GET.get('category')
        limit = min(int(request.GET.get('limit', 20)), 100)
        
        user_location = Point(lng, lat, srid=4326)
        
        # Filter businesses with valid coordinates
        qs = Business.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False,
            is_active=True
        )
        
        if category:
            qs = qs.filter(category_id=category)
        
        # Calculate distance
        from django.db.models import F, ExpressionWrapper
        from django.db.models.fields import FloatField
        from math import radians, cos, sin, asin, sqrt
        
        # Haversine formula in SQL
        qs = qs.extra(
            select={
                'distance': '''
                    6371 * acos(
                        cos(radians(%s)) * cos(radians(latitude)) * 
                        cos(radians(longitude) - radians(%s)) + 
                        sin(radians(%s)) * sin(radians(latitude))
                    )
                '''
            },
            select_params=[lat, lng, lat]
        )
        
        # Filter by radius and sort by distance
        qs = qs.extra(where=['distance <= %s'], params=[radius])
        qs = qs.order_by('distance')[:limit]
        
        serializer = self.get_serializer(qs, many=True)
        return Response({
            'count': qs.count(),
            'results': serializer.data
        })
```

---

## 🟡 Medium Priority - لتطبيق Business Owner

### 4️⃣ Owner Dashboard API

**الملف:** `apps/api/views/business_owner.py` (موجود لكن محتاج تحسين)  
**الأولوية:** 🟡 متوسطة  
**الوقت:** 1.5 يوم

#### ❌ المطلوب:

```python
# Owner Dashboard Summary
GET /api/v1/owner/dashboard/

Response:
{
  "total_businesses": 3,
  "total_views": 1250,
  "total_reviews": 45,
  "average_rating": 4.3,
  "total_favorites": 28,
  "active_deals": 5,
  "total_products": 120,
  "pending_reviews": 3,
  "views_this_week": 180,
  "views_trend": "+15%",
  "recent_reviews": [...],  // last 5
  "top_businesses": [...]   // by views
}

# Owner Statistics
GET /api/v1/owner/statistics/

Query Parameters:
  - business_id (optional)
  - start_date (optional)
  - end_date (optional)
  - period: day,week,month,year (optional)

Response:
{
  "views_over_time": [
    {"date": "2026-02-01", "count": 45},
    {"date": "2026-02-02", "count": 52},
    ...
  ],
  "reviews_distribution": {
    "5_star": 20,
    "4_star": 15,
    "3_star": 8,
    "2_star": 2,
    "1_star": 0
  },
  "top_products": [
    {"id": 1, "name": "...", "views": 150},
    ...
  ],
  "peak_hours": [...]
}
```

**Implementation:**
```python
# apps/api/views/business_owner.py

from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

class OwnerDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        businesses = Business.objects.filter(owner=user)
        
        # Calculate statistics
        total_views = businesses.aggregate(Sum('view_count'))['view_count__sum'] or 0
        total_reviews = Review.objects.filter(business__owner=user).count()
        avg_rating = Review.objects.filter(
            business__owner=user
        ).aggregate(Avg('rating'))['rating__avg'] or 0
        
        # This week statistics
        week_ago = timezone.now() - timedelta(days=7)
        # Assume ViewLog model exists
        views_this_week = ViewLog.objects.filter(
            business__owner=user,
            created_at__gte=week_ago
        ).count()
        
        # Previous week for trend
        two_weeks_ago = timezone.now() - timedelta(days=14)
        views_prev_week = ViewLog.objects.filter(
            business__owner=user,
            created_at__gte=two_weeks_ago,
            created_at__lt=week_ago
        ).count()
        
        trend = ((views_this_week - views_prev_week) / views_prev_week * 100) \
                if views_prev_week > 0 else 0
        
        # Recent reviews
        recent_reviews = Review.objects.filter(
            business__owner=user
        ).order_by('-created_at')[:5]
        
        return Response({
            'total_businesses': businesses.count(),
            'total_views': total_views,
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 1),
            'total_favorites': Favorite.objects.filter(
                business__owner=user
            ).count(),
            'active_deals': Deal.objects.filter(
                business__owner=user,
                is_active=True
            ).count(),
            'total_products': Product.objects.filter(
                business__owner=user
            ).count(),
            'views_this_week': views_this_week,
            'views_trend': f"+{trend:.0f}%" if trend > 0 else f"{trend:.0f}%",
            'recent_reviews': ReviewSerializer(recent_reviews, many=True).data,
        })
```

---

### 5️⃣ Owner Reviews Management

**الملف:** `apps/api/views/business_owner.py`  
**الأولوية:** 🟡 متوسطة  
**الوقت:** 0.5 يوم

```python
# Get all my reviews
GET /api/v1/owner/reviews/
Query: ?business_id=...&rating=...&has_reply=true/false

# Respond to review
POST /api/v1/owner/reviews/{id}/respond/
{
  "reply": "نشكركم على تقييمكم"
}
```

---

### 6️⃣ Product Bulk Operations

**الملف:** `apps/api/views/products.py`  
**الأولوية:** 🟡 متوسطة  
**الوقت:** 0.5 يوم

```python
# Toggle availability
PATCH /api/v1/products/{id}/toggle-availability/

# Bulk price update
POST /api/v1/products/bulk-update/
[
  {"id": 1, "price": 150.00, "discount": 10},
  {"id": 2, "price": 200.00},
  ...
]
```

---

## 🟢 Low Priority - لتطبيق Admin

### 7️⃣ Admin Dashboard API

**الملف:** `apps/api/views/admin.py` (موجود جزئياً)  
**الأولوية:** 🟢 منخفضة  
**الوقت:** 1 يوم

```python
# Admin Dashboard
GET /api/v1/admin/dashboard/

Response:
{
  "total_users": 5000,
  "total_businesses": 1200,
  "total_products": 8500,
  "total_deals": 450,
  "pending_verifications": 15,
  "pending_reviews": 8,
  "users_growth": [...],
  "revenue_stats": {...},
  "recent_registrations": [...]
}

# Admin Statistics
GET /api/v1/admin/statistics/?period=month
```

---

### 8️⃣ Admin Management Actions

**الملف:** `apps/api/views/admin.py`  
**الأولوية:** 🟢 منخفضة  
**الوقت:** 1 يوم

```python
# Verify business
POST /api/v2/admin/businesses/{id}/verify/

# Feature business
POST /api/v2/admin/businesses/{id}/feature/

# Approve/Reject review
POST /api/v2/admin/reviews/{id}/approve/
POST /api/v2/admin/reviews/{id}/reject/

# Toggle user active status
POST /api/v2/admin/users/{id}/toggle-active/
```

---

## 🔟 Future Features - مستقبلي

### 9️⃣ Notifications API

**الملف:** `apps/api/views/notifications.py` (جديد)  
**الأولوية:** 🔵 مستقبلي  
**الوقت:** 2 أيام

```python
GET /api/v1/notifications/
POST /api/v1/notifications/{id}/mark-read/
POST /api/v1/notifications/mark-all-read/
DELETE /api/v1/notifications/{id}/
```

---

## 📅 خطة التنفيذ المقترحة

### الأسبوع الأول - High Priority APIs

**اليوم 1-2:**
- ✅ Reviews API إكمال (CREATE, UPDATE, DELETE, REPLY)
- ✅ Testing & Documentation

**اليوم 3-4:**
- ✅ Advanced Search API
- ✅ Nearby Businesses API
- ✅ Testing

**اليوم 5:**
- ✅ Code Review
- ✅ Performance Testing
- ✅ Update API Documentation

### الأسبوع الثاني - Medium Priority APIs

**اليوم 1-2:**
- ✅ Owner Dashboard API
- ✅ Owner Statistics API

**اليوم 3:**
- ✅ Owner Reviews Management
- ✅ Product Bulk Operations

**اليوم 4:**
- ✅ Admin Dashboard API
- ✅ Admin Management Actions

**اليوم 5:**
- ✅ Final Testing
- ✅ Update Documentation
- ✅ Deploy to Production

---

## 🧪 الاختبار والتوثيق

### Testing Checklist

```bash
# 1. Unit Tests
python manage.py test apps.api.tests

# 2. Manual Testing with Postman/cURL
# Test each endpoint

# 3. Load Testing
# Use locust or similar

# 4. Documentation
# Update Swagger docs
python manage.py spectacular --file schema.yml
```

### API Documentation

تحديث `apps/api/README.md` بكل ال endpoints الجديدة.

---

## 📝 ملاحظات مهمة

### Performance Optimization

1. **Database Indexes:**
```python
# Add to models
class Business(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['category', 'city']),
            models.Index(fields=['is_featured', '-created_at']),
        ]
```

2. **Caching:**
```python
from django.core.cache import cache

# Cache expensive queries
cached_data = cache.get('dashboard_stats_{}'.format(user.id))
if not cached_data:
    cached_data = calculate_stats(user)
    cache.set('dashboard_stats_{}'.format(user.id), cached_data, 300)  # 5 min
```

3. **Select Related / Prefetch Related:**
```python
# Always use for FK/M2M
qs = Business.objects.select_related('category', 'owner').prefetch_related('products')
```

### Security

1. **Rate Limiting:**
```python
# Add to settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

2. **Input Validation:**
```python
# Always validate user input
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
```

---

## ✅ Summary Checklist

### High Priority (أسبوع 1)
- [ ] Reviews API - Create
- [ ] Reviews API - Update/Delete
- [ ] Reviews API - Owner Reply
- [ ] Advanced Search API
- [ ] Nearby Businesses API

### Medium Priority (أسبوع 2)
- [ ] Owner Dashboard API
- [ ] Owner Statistics API
- [ ] Owner Reviews Management
- [ ] Product Bulk Operations
- [ ] Admin Dashboard API
- [ ] Admin Management Actions

### Documentation
- [ ] Update API README
- [ ] Update Swagger/OpenAPI docs
- [ ] Create Postman Collection
- [ ] Write Integration Guide for Flutter

---

**تاريخ الإنشاء:** 15 فبراير 2026  
**آخر تحديث:** 15 فبراير 2026  
**الحالة:** 🔴 In Progress
