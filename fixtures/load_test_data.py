#!/usr/bin/env python
"""
Script to load comprehensive test data for dashboard testing

Usage:
    python fixtures/load_test_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.directory.models import Business, Governorate, City, District
from apps.categories.models import Category
from apps.products.models import Product
from apps.deals.models import Deal
from apps.reviews.models import Review, ReviewReply
from apps.subscriptions.models import SubscriptionPlan, Subscription

User = get_user_model()


def create_users():
    """إنشاء مستخدمين تجريبيين"""
    print("✅ إنشاء المستخدمين...")
    
    # Business owners
    owners = [
        {'username': 'ahmed_owner', 'email': 'ahmed@test.com', 'phone': '+966501234567', 'first_name': 'أحمد', 'last_name': 'محمد', 'password': 'test123'},
        {'username': 'fatima_owner', 'email': 'fatima@test.com', 'phone': '+966501234568', 'first_name': 'فاطمة', 'last_name': 'علي', 'password': 'test123'},
        {'username': 'khaled_owner', 'email': 'khaled@test.com', 'phone': '+966501234569', 'first_name': 'خالد', 'last_name': 'حسن', 'password': 'test123'},
        {'username': 'maha_owner', 'email': 'maha@test.com', 'phone': '+966501234570', 'first_name': 'مها', 'last_name': 'عبدالله', 'password': 'test123'},
        {'username': 'omar_owner', 'email': 'omar@test.com', 'phone': '+966501234571', 'first_name': 'عمر', 'last_name': 'سعيد', 'password': 'test123'},
    ]
    
    created_owners = []
    for owner_data in owners:
        user, created = User.objects.get_or_create(
            username=owner_data['username'],
            defaults={
                'email': owner_data['email'],
                'phone': owner_data['phone'],
                'first_name': owner_data['first_name'],
                'last_name': owner_data['last_name'],
            }
        )
        if created:
            user.set_password(owner_data['password'])
            user.save()
            print(f"  - تم إنشاء: {user.get_full_name()} ({user.username})")
        created_owners.append(user)
    
    # Customers
    customers_data = [
        {'username': 'customer1', 'phone': '+966502234567', 'first_name': 'محمد', 'last_name': 'أحمد'},
        {'username': 'customer2', 'phone': '+966502234568', 'first_name': 'سارة', 'last_name': 'خالد'},
        {'username': 'customer3', 'phone': '+966502234569', 'first_name': 'يوسف', 'last_name': 'محمود'},
        {'username': 'customer4', 'phone': '+966502234570', 'first_name': 'نور', 'last_name': 'عبدالرحمن'},
        {'username': 'customer5', 'phone': '+966502234571', 'first_name': 'ليلى', 'last_name': 'حسين'},
        {'username': 'customer6', 'phone': '+966502234572', 'first_name': 'عبدالله', 'last_name': 'عمر'},
        {'username': 'customer7', 'phone': '+966502234573', 'first_name': 'مريم', 'last_name': 'فاروق'},
        {'username': 'customer8', 'phone': '+966502234574', 'first_name': 'طارق', 'last_name': 'رشيد'},
        {'username': 'customer9', 'phone': '+966502234575', 'first_name': 'هدى', 'last_name': 'عبدالعزيز'},
        {'username': 'customer10', 'phone': '+966502234576', 'first_name': 'كريم', 'last_name': 'السيد'},
    ]
    
    created_customers = []
    for customer_data in customers_data:
        user, created = User.objects.get_or_create(
            username=customer_data['username'],
            defaults={
                'email': f"{customer_data['username']}@test.com",
                'phone': customer_data['phone'],
                'first_name': customer_data['first_name'],
                'last_name': customer_data['last_name'],
            }
        )
        if created:
            user.set_password('test123')
            user.save()
        created_customers.append(user)
    
    print(f"  ✅ تم إنشاء {len(created_owners)} أصحاب محلات و {len(created_customers)} عميل")
    return created_owners, created_customers


def create_locations():
    """إنشاء مواقع جغرافية"""
    print("✅ إنشاء المواقع...")
    
    # Riyadh
    riyadh_gov, _ = Governorate.objects.get_or_create(
        name_ar='الرياض',
        defaults={'name_en': 'Riyadh'}
    )
    riyadh_city, _ = City.objects.get_or_create(
        governorate=riyadh_gov,
        name_ar='الرياض',
        defaults={'name_en': 'Riyadh'}
    )
    
    districts = [
        {'name_ar': 'العليا', 'name_en': 'Al Olaya'},
        {'name_ar': 'الملز', 'name_en': 'Al Malaz'},
        {'name_ar': 'النخيل', 'name_en': 'Al Nakheel'},
        {'name_ar': 'العقيق', 'name_en': 'Al Aqeeq'},
        {'name_ar': 'الربوة', 'name_en': 'Al Rabwah'},
    ]
    
    created_districts = []
    for district_data in districts:
        district, _ = District.objects.get_or_create(
            city=riyadh_city,
            name_ar=district_data['name_ar'],
            defaults={'name_en': district_data['name_en']}
        )
        created_districts.append(district)
    
    print(f"  ✅ تم إنشاء {len(created_districts)} حي")
    return created_districts


def create_categories():
    """إنشاء فئات"""
    print("✅ إنشاء الفئات...")
    
    categories_data = [
        {'name_ar': 'مطاعم', 'name_en': 'Restaurants', 'icon': 'fa-utensils'},
        {'name_ar': 'مقاهي', 'name_en': 'Cafes', 'icon': 'fa-coffee'},
        {'name_ar': 'تسوق', 'name_en': 'Shopping', 'icon': 'fa-shopping-bag'},
        {'name_ar': 'تقنية', 'name_en': 'Technology', 'icon': 'fa-laptop'},
        {'name_ar': 'صحة', 'name_en': 'Health', 'icon': 'fa-heartbeat'},
        {'name_ar': 'تعليم', 'name_en': 'Education', 'icon': 'fa-graduation-cap'},
        {'name_ar': 'سيارات', 'name_en': 'Automotive', 'icon': 'fa-car'},
        {'name_ar': 'عقارات', 'name_en': 'Real Estate', 'icon': 'fa-building'},
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category, _ = Category.objects.get_or_create(
            name_ar=cat_data['name_ar'],
            defaults={
                'name_en': cat_data['name_en'],
                'icon': cat_data['icon'],
                'is_active': True,
            }
        )
        created_categories.append(category)
    
    print(f"  ✅ تم إنشاء {len(created_categories)} فئة")
    return created_categories


def create_businesses(owners, districts, categories):
    """إنشاء محلات تجارية"""
    print("✅ إنشاء المحلات...")
    
    businesses_data = [
        {'name_ar': 'مطعم الفخامة', 'name_en': 'Al Fakhamah Restaurant', 'category': 0, 'owner': 0},
        {'name_ar': 'مقهى الرياض', 'name_en': 'Riyadh Cafe', 'category': 1, 'owner': 1},
        {'name_ar': 'محل الأناقة', 'name_en': 'Elegance Store', 'category': 2, 'owner': 2},
        {'name_ar': 'مركز التقنية الحديثة', 'name_en': 'Modern Tech Center', 'category': 3, 'owner': 3},
        {'name_ar': 'عيادة النور', 'name_en': 'Al Noor Clinic', 'category': 4, 'owner': 4},
        {'name_ar': 'مطعم العرين', 'name_en': 'Al Areen Restaurant', 'category': 0, 'owner': 0},
        {'name_ar': 'مقهى الزاوية', 'name_en': 'Corner Cafe', 'category': 1, 'owner': 1},
        {'name_ar': 'بوتيك الموضة', 'name_en': 'Fashion Boutique', 'category': 2, 'owner': 2},
        {'name_ar': 'معهد المستقبل', 'name_en': 'Future Institute', 'category': 5, 'owner': 3},
        {'name_ar': 'ورشة النجم', 'name_en': 'Star Workshop', 'category': 6, 'owner': 4},
    ]
    
    created_businesses = []
    for i, bus_data in enumerate(businesses_data):
        business, created = Business.objects.get_or_create(
            slug=f"business-{i+1}",
            defaults={
                'name_ar': bus_data['name_ar'],
                'name_en': bus_data['name_en'],
                'description_ar': f"وصف {bus_data['name_ar']} - نقدم أفضل الخدمات بجودة عالية",
                'description_en': f"Description of {bus_data['name_en']} - We provide the best services with high quality",
                'owner': owners[bus_data['owner']],
                'category': categories[bus_data['category']],
                'district': districts[i % len(districts)],
                'address_ar': f"شارع الملك فهد ، {districts[i % len(districts)].name_ar}",
                'address_en': f"King Fahd Street, {districts[i % len(districts)].name_en}",
                'phone': f"+966555{i:06d}",
                'email': f"info@business{i+1}.com",
                'website': f"https://business{i+1}.com",
                'is_active': True,
                'is_verified': True,
                'is_featured': i < 3,
            }
        )
        created_businesses.append(business)
    
    print(f"  ✅ تم إنشاء {len(created_businesses)} محل")
    return created_businesses


def create_products(businesses):
    """إنشاء منتجات وخدمات"""
    print("✅ إنشاء المنتجات...")
    
    products_data = [
        {'name_ar': 'وجبة شاورما', 'name_en': 'Shawarma Meal', 'type': 'product', 'price': 25},
        {'name_ar': 'فنجان قهوة', 'name_en': 'Cup of Coffee', 'type': 'product', 'price': 15},
        {'name_ar': 'فستان سهرة', 'name_en': 'Evening Dress', 'type': 'product', 'price': 350},
        {'name_ar': 'لاب توب', 'name_en': 'Laptop', 'type': 'product', 'price': 3500},
        {'name_ar': 'فحص طبي', 'name_en': 'Medical Checkup', 'type': 'service', 'price': 200},
        {'name_ar': 'برجر لحم', 'name_en': 'Beef Burger', 'type': 'product', 'price': 35},
        {'name_ar': 'عصير طبيعي', 'name_en': 'Fresh Juice', 'type': 'product', 'price': 18},
        {'name_ar': 'بذلة رسمية', 'name_en': 'Formal Suit', 'type': 'product', 'price': 800},
        {'name_ar': 'هاتف ذكي', 'name_en': 'Smartphone', 'type': 'product', 'price': 2500},
        {'name_ar': 'دورة تدريبية', 'name_en': 'Training Course', 'type': 'service', 'price': 1500},
    ]
    
    created_products = []
    for i, prod_data in enumerate(products_data):
        business = businesses[i % len(businesses)]
        product, created = Product.objects.get_or_create(
            slug=f"product-{i+1}",
            defaults={
                'name_ar': prod_data['name_ar'],
                'name_en': prod_data['name_en'],
                'description_ar': f"وصف {prod_data['name_ar']} - منتج عالي الجودة",
                'description_en': f"Description of {prod_data['name_en']} - High quality product",
                'business': business,
                'product_type': prod_data['type'],
                'price': Decimal(str(prod_data['price'])),
                'is_available': True,
            }
        )
        created_products.append(product)
    
    print(f"  ✅ تم إنشاء {len(created_products)} منتج/خدمة")
    return created_products


def create_deals(businesses):
    """إنشاء عروض"""
    print("✅ إنشاء العروض...")
    
    now = datetime.now()
    
    deals_data = [
        # Active deals
        {'title_ar': 'خصم 50% على الوجبات', 'title_en': '50% Off on Meals', 'discount': 50, 'start': now - timedelta(days=5), 'end': now + timedelta(days=10)},
        {'title_ar': 'عرض اشتر 2 واحصل على 1 مجاناً', 'title_en': 'Buy 2 Get 1 Free', 'discount': 33, 'start': now - timedelta(days=3), 'end': now + timedelta(days=7)},
        {'title_ar': 'خصم العودة للمدارس', 'title_en': 'Back to School Discount', 'discount': 30, 'start': now - timedelta(days=2), 'end': now + timedelta(days=20)},
        
        # Upcoming deals
        {'title_ar': 'عرض عيد الفطر', 'title_en': 'Eid Al Fitr Offer', 'discount': 40, 'start': now + timedelta(days=5), 'end': now + timedelta(days=15)},
        {'title_ar': 'عرض الصيف', 'title_en': 'Summer Sale', 'discount': 60, 'start': now + timedelta(days=10), 'end': now + timedelta(days=30)},
        
        # Expired deals
        {'title_ar': 'عرض رمضان', 'title_en': 'Ramadan Offer', 'discount': 25, 'start': now - timedelta(days=30), 'end': now - timedelta(days=5)},
        {'title_ar': 'خصم الشتاء', 'title_en': 'Winter Discount', 'discount': 35, 'start': now - timedelta(days=60), 'end': now - timedelta(days=10)},
    ]
    
    created_deals = []
    for i, deal_data in enumerate(deals_data):
        business = businesses[i % len(businesses)]
        deal, created = Deal.objects.get_or_create(
            slug=f"deal-{i+1}",
            defaults={
                'title_ar': deal_data['title_ar'],
                'title_en': deal_data['title_en'],
                'description_ar': f"وصف {deal_data['title_ar']}",
                'description_en': f"Description of {deal_data['title_en']}",
                'business': business,
                'deal_type': 'percentage',
                'discount_percentage': deal_data['discount'],
                'start_date': deal_data['start'],
                'end_date': deal_data['end'],
            }
        )
        created_deals.append(deal)
    
    print(f"  ✅ تم إنشاء {len(created_deals)} عرض")
    return created_deals


def create_reviews(businesses, customers):
    """إنشاء تقييمات"""
    print("✅ إنشاء التقييمات...")
    
    comments = [
        'تجربة رائعة وخدمة ممتازة!',
        'أنصح به بشدة، جودة عالية',
        'خدمة جيدة لكن الأسعار مرتفعة قليلاً',
        'ممتاز جداً، سأعود بالتأكيد',
        'تجربة معقولة، يحتاج تحسين',
        'رائع ونظيف وموظفين محترفين',
        'جودة ممتازة وأسعار مناسبة',
        'خدمة سريعة ومريحة',
    ]
    
    created_reviews = []
    review_count = 0
    
    for business in businesses[:5]:  # First 5 businesses
        for i in range(5):  # 5 reviews each
            if review_count >= len(customers):
                break
            
            customer = customers[review_count % len(customers)]
            rating = [5, 5, 4, 4, 3][i]  # Mix of ratings
            
            review, created = Review.objects.get_or_create(
                business=business,
                user=customer,
                defaults={
                    'rating': rating,
                    'comment': comments[review_count % len(comments)],
                    'is_approved': True,
                }
            )
            
            # Add reply for some reviews
            if i < 2:  # Reply to first 2 reviews
                ReviewReply.objects.get_or_create(
                    review=review,
                    defaults={
                        'user': business.owner,
                        'comment': 'شكراً لتقييمك، نسعى دائماً لتقديم الأفضل!',
                    }
                )
            
            created_reviews.append(review)
            review_count += 1
    
    print(f"  ✅ تم إنشاء {len(created_reviews)} تقييم")
    return created_reviews


def main():
    """الدالة الرئيسية"""
    print("✨ بدء تحميل البيانات التجريبية...\n")
    
    # Create data
    owners, customers = create_users()
    districts = create_locations()
    categories = create_categories()
    businesses = create_businesses(owners, districts, categories)
    products = create_products(businesses)
    deals = create_deals(businesses)
    reviews = create_reviews(businesses, customers)
    
    print("\n✨ تم تحميل جميع البيانات بنجاح!")
    print("\n🔑 بيانات الدخول:")
    print("  - المستخدم: ahmed_owner")
    print("  - كلمة المرور: test123")
    print("\nأو استخدم:")
    print("  - fatima_owner / khaled_owner / maha_owner / omar_owner")
    print("  - كلمة المرور: test123")
    print("\n🚀 يمكنك الآن الدخول واختبار لوحة التحكم!")


if __name__ == '__main__':
    main()
