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
import random


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
        {'username': 'ahmed_owner', 'email': 'ahmed@test.com', 'phone': '+20101234567', 'first_name': 'أحمد', 'last_name': 'محمد', 'password': 'test123'},
        {'username': 'fatima_owner', 'email': 'fatima@test.com', 'phone': '+20101234568', 'first_name': 'فاطمة', 'last_name': 'علي', 'password': 'test123'},
        {'username': 'khaled_owner', 'email': 'khaled@test.com', 'phone': '+20101234569', 'first_name': 'خالد', 'last_name': 'حسن', 'password': 'test123'},
        {'username': 'maha_owner', 'email': 'maha@test.com', 'phone': '+20101234570', 'first_name': 'مها', 'last_name': 'عبدالله', 'password': 'test123'},
        {'username': 'omar_owner', 'email': 'omar@test.com', 'phone': '+20101234571', 'first_name': 'عمر', 'last_name': 'سعيد', 'password': 'test123'},
        {'username': 'nour_owner', 'email': 'nour@test.com', 'phone': '+20101234572', 'first_name': 'نور', 'last_name': 'حسين', 'password': 'test123'},
        {'username': 'sara_owner', 'email': 'sara@test.com', 'phone': '+20101234573', 'first_name': 'سارة', 'last_name': 'عبدالرحمن', 'password': 'test123'},
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
        {'username': 'customer1', 'phone': '+20102234567', 'first_name': 'محمد', 'last_name': 'أحمد'},
        {'username': 'customer2', 'phone': '+20102234568', 'first_name': 'سارة', 'last_name': 'خالد'},
        {'username': 'customer3', 'phone': '+20102234569', 'first_name': 'يوسف', 'last_name': 'محمود'},
        {'username': 'customer4', 'phone': '+20102234570', 'first_name': 'نور', 'last_name': 'عبدالرحمن'},
        {'username': 'customer5', 'phone': '+20102234571', 'first_name': 'ليلى', 'last_name': 'حسين'},
        {'username': 'customer6', 'phone': '+20102234572', 'first_name': 'عبدالله', 'last_name': 'عمر'},
        {'username': 'customer7', 'phone': '+20102234573', 'first_name': 'مريم', 'last_name': 'فاروق'},
        {'username': 'customer8', 'phone': '+20102234574', 'first_name': 'طارق', 'last_name': 'رشيد'},
        {'username': 'customer9', 'phone': '+20102234575', 'first_name': 'هدى', 'last_name': 'عبدالعزيز'},
        {'username': 'customer10', 'phone': '+20102234576', 'first_name': 'كريم', 'last_name': 'السيد'},
        {'username': 'customer11', 'phone': '+20102234577', 'first_name': 'ياسمين', 'last_name': 'عادل'},
        {'username': 'customer12', 'phone': '+20102234578', 'first_name': 'حسن', 'last_name': 'علي'},
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
    """إنشاء مواقع جغرافية - محافظات قناة السويس"""
    print("✅ إنشاء المواقع الجغرافية...")
    
    all_districts = []
    
    # ========== محافظة الإسماعيلية ==========
    # استخدام filter بدلاً من get_or_create لتجنب UNIQUE constraint
    ismailia_gov = Governorate.objects.filter(name_ar='الإسماعيلية').first()
    if not ismailia_gov:
        ismailia_gov = Governorate.objects.create(
            name_ar='الإسماعيلية',
            name_en='Ismailia'
        )
        print(f"  - تم إنشاء محافظة: الإسماعيلية")
    
    ismailia_cities = [
        {'name_ar': 'الإسماعيلية', 'name_en': 'Ismailia', 'districts': [
            {'name_ar': 'الشيخ زايد', 'name_en': 'Sheikh Zayed'},
            {'name_ar': 'حي السلام', 'name_en': 'Al Salam'},
            {'name_ar': 'حي الضواحي', 'name_en': 'Al Dawahy'},
            {'name_ar': 'المستقبل', 'name_en': 'Al Mostakbal'},
            {'name_ar': 'عرب المعادي', 'name_en': 'Arab Al Maadi'},
        ]},
        {'name_ar': 'فايد', 'name_en': 'Fayed', 'districts': [
            {'name_ar': 'وسط فايد', 'name_en': 'Fayed Center'},
            {'name_ar': 'الشاطئ', 'name_en': 'Beach Area'},
        ]},
        {'name_ar': 'القنطرة شرق', 'name_en': 'Qantara East', 'districts': [
            {'name_ar': 'وسط القنطرة', 'name_en': 'Qantara Center'},
        ]},
    ]
    
    for city_data in ismailia_cities:
        city = City.objects.filter(
            governorate=ismailia_gov,
            name_ar=city_data['name_ar']
        ).first()
        if not city:
            city = City.objects.create(
                governorate=ismailia_gov,
                name_ar=city_data['name_ar'],
                name_en=city_data['name_en']
            )
        
        for district_data in city_data['districts']:
            district = District.objects.filter(
                city=city,
                name_ar=district_data['name_ar']
            ).first()
            if not district:
                district = District.objects.create(
                    city=city,
                    name_ar=district_data['name_ar'],
                    name_en=district_data['name_en']
                )
            all_districts.append(district)
    
    # ========== محافظة بورسعيد ==========
    portsaid_gov = Governorate.objects.filter(name_ar='بورسعيد').first()
    if not portsaid_gov:
        portsaid_gov = Governorate.objects.create(
            name_ar='بورسعيد',
            name_en='Port Said'
        )
        print(f"  - تم إنشاء محافظة: بورسعيد")
    
    portsaid_cities = [
        {'name_ar': 'بورسعيد', 'name_en': 'Port Said', 'districts': [
            {'name_ar': 'حي الشرق', 'name_en': 'East District'},
            {'name_ar': 'حي العرب', 'name_en': 'Al Arab'},
            {'name_ar': 'حي الزهور', 'name_en': 'Al Zohour'},
            {'name_ar': 'حي المناخ', 'name_en': 'Al Manakh'},
            {'name_ar': 'بورفؤاد', 'name_en': 'Port Fouad'},
            {'name_ar': 'حي الضواحي', 'name_en': 'Al Dawahy'},
        ]},
    ]
    
    for city_data in portsaid_cities:
        city = City.objects.filter(
            governorate=portsaid_gov,
            name_ar=city_data['name_ar']
        ).first()
        if not city:
            city = City.objects.create(
                governorate=portsaid_gov,
                name_ar=city_data['name_ar'],
                name_en=city_data['name_en']
            )
        
        for district_data in city_data['districts']:
            district = District.objects.filter(
                city=city,
                name_ar=district_data['name_ar']
            ).first()
            if not district:
                district = District.objects.create(
                    city=city,
                    name_ar=district_data['name_ar'],
                    name_en=district_data['name_en']
                )
            all_districts.append(district)
    
    # ========== محافظة السويس ==========
    suez_gov = Governorate.objects.filter(name_ar='السويس').first()
    if not suez_gov:
        suez_gov = Governorate.objects.create(
            name_ar='السويس',
            name_en='Suez'
        )
        print(f"  - تم إنشاء محافظة: السويس")
    
    suez_cities = [
        {'name_ar': 'السويس', 'name_en': 'Suez', 'districts': [
            {'name_ar': 'حي الأربعين', 'name_en': 'Al Arbaeen'},
            {'name_ar': 'حي السلام', 'name_en': 'Al Salam'},
            {'name_ar': 'حي فيصل', 'name_en': 'Faisal'},
            {'name_ar': 'حي الجناين', 'name_en': 'Al Ganayem'},
            {'name_ar': 'عتاقة', 'name_en': 'Ataqah'},
        ]},
    ]
    
    for city_data in suez_cities:
        city = City.objects.filter(
            governorate=suez_gov,
            name_ar=city_data['name_ar']
        ).first()
        if not city:
            city = City.objects.create(
                governorate=suez_gov,
                name_ar=city_data['name_ar'],
                name_en=city_data['name_en']
            )
        
        for district_data in city_data['districts']:
            district = District.objects.filter(
                city=city,
                name_ar=district_data['name_ar']
            ).first()
            if not district:
                district = District.objects.create(
                    city=city,
                    name_ar=district_data['name_ar'],
                    name_en=district_data['name_en']
                )
            all_districts.append(district)
    
    print(f"  ✅ تم إنشاء 3 محافظات و {len(all_districts)} حي")
    return all_districts



def create_categories():
    """إنشاء فئات شاملة مع تصحيح الأيقونات"""
    print("✅ إنشاء الفئات...")
    
    categories_data = [
        # مطاعم وكافيهات
        {'name_ar': 'مطاعم', 'name_en': 'Restaurants', 'icon': 'fas fa-utensils'},
        {'name_ar': 'مقاهي', 'name_en': 'Cafes', 'icon': 'fas fa-coffee'},
        {'name_ar': 'حلويات', 'name_en': 'Sweets', 'icon': 'fas fa-birthday-cake'},
        {'name_ar': 'مطاعم سريعة', 'name_en': 'Fast Food', 'icon': 'fas fa-hamburger'},
        
        # تسوق
        {'name_ar': 'تسوق وأزياء', 'name_en': 'Shopping & Fashion', 'icon': 'fas fa-shopping-bag'},
        {'name_ar': 'إلكترونيات', 'name_en': 'Electronics', 'icon': 'fas fa-laptop'},
        {'name_ar': 'أثاث ومفروشات', 'name_en': 'Furniture', 'icon': 'fas fa-couch'},
        {'name_ar': 'مجوهرات', 'name_en': 'Jewelry', 'icon': 'fas fa-gem'},
        {'name_ar': 'كتب ومكتبات', 'name_en': 'Books & Stationery', 'icon': 'fas fa-book'},
        
        # خدمات صحية
        {'name_ar': 'مستشفيات', 'name_en': 'Hospitals', 'icon': 'fas fa-hospital'},
        {'name_ar': 'عيادات طبية', 'name_en': 'Medical Clinics', 'icon': 'fas fa-stethoscope'},
        {'name_ar': 'صيدليات', 'name_en': 'Pharmacies', 'icon': 'fas fa-pills'},
        {'name_ar': 'مراكز أسنان', 'name_en': 'Dental Centers', 'icon': 'fas fa-tooth'},
        {'name_ar': 'مختبرات طبية', 'name_en': 'Medical Labs', 'icon': 'fas fa-flask'},
        
        # تعليم
        {'name_ar': 'مدارس', 'name_en': 'Schools', 'icon': 'fas fa-school'},
        {'name_ar': 'جامعات', 'name_en': 'Universities', 'icon': 'fas fa-university'},
        {'name_ar': 'معاهد تدريب', 'name_en': 'Training Centers', 'icon': 'fas fa-graduation-cap'},
        {'name_ar': 'حضانات', 'name_en': 'Nurseries', 'icon': 'fas fa-child'},
        
        # خدمات سيارات
        {'name_ar': 'معارض سيارات', 'name_en': 'Car Showrooms', 'icon': 'fas fa-car'},
        {'name_ar': 'ورش صيانة', 'name_en': 'Car Service', 'icon': 'fas fa-wrench'},
        {'name_ar': 'غسيل سيارات', 'name_en': 'Car Wash', 'icon': 'fas fa-car-wash'},
        {'name_ar': 'قطع غيار', 'name_en': 'Auto Parts', 'icon': 'fas fa-tools'},
        
        # عقارات وإنشاءات
        {'name_ar': 'عقارات', 'name_en': 'Real Estate', 'icon': 'fas fa-building'},
        {'name_ar': 'شركات مقاولات', 'name_en': 'Construction', 'icon': 'fas fa-hard-hat'},
        {'name_ar': 'ديكور وتصميم', 'name_en': 'Interior Design', 'icon': 'fas fa-paint-roller'},
        
        # جمال وعناية
        {'name_ar': 'صالونات تجميل', 'name_en': 'Beauty Salons', 'icon': 'fas fa-cut'},
        {'name_ar': 'صالونات رجالي', 'name_en': 'Barber Shops', 'icon': 'fas fa-male'},
        {'name_ar': 'سبا ومساج', 'name_en': 'Spa & Massage', 'icon': 'fas fa-spa'},
        
        # رياضة ولياقة
        {'name_ar': 'نوادي رياضية', 'name_en': 'Gyms & Fitness', 'icon': 'fas fa-dumbbell'},
        {'name_ar': 'ملاعب رياضية', 'name_en': 'Sports Fields', 'icon': 'fas fa-futbol'},
        
        # ترفيه وسياحة
        {'name_ar': 'فنادق', 'name_en': 'Hotels', 'icon': 'fas fa-hotel'},
        {'name_ar': 'منتجعات سياحية', 'name_en': 'Resorts', 'icon': 'fas fa-umbrella-beach'},
        {'name_ar': 'حدائق', 'name_en': 'Parks & Gardens', 'icon': 'fas fa-tree'},
        {'name_ar': 'شواطئ', 'name_en': 'Beaches', 'icon': 'fas fa-water'},
        {'name_ar': 'دور سينما', 'name_en': 'Cinemas', 'icon': 'fas fa-film'},
        {'name_ar': 'مراكز ترفيه', 'name_en': 'Entertainment Centers', 'icon': 'fas fa-gamepad'},
        
        # أماكن عبادة
        {'name_ar': 'مساجد', 'name_en': 'Mosques', 'icon': 'fas fa-mosque'},
        {'name_ar': 'كنائس', 'name_en': 'Churches', 'icon': 'fas fa-church'},
        
        # خدمات عامة
        {'name_ar': 'بنوك', 'name_en': 'Banks', 'icon': 'fas fa-university'},
        {'name_ar': 'مكاتب بريد', 'name_en': 'Post Offices', 'icon': 'fas fa-envelope'},
        {'name_ar': 'محطات وقود', 'name_en': 'Gas Stations', 'icon': 'fas fa-gas-pump'},
        {'name_ar': 'محلات سوبر ماركت', 'name_en': 'Supermarkets', 'icon': 'fas fa-shopping-cart'},
        
        # خدمات أخرى
        {'name_ar': 'مطابع', 'name_en': 'Printing Services', 'icon': 'fas fa-print'},
        {'name_ar': 'استوديوهات تصوير', 'name_en': 'Photo Studios', 'icon': 'fas fa-camera'},
        {'name_ar': 'شحن ونقل', 'name_en': 'Shipping & Logistics', 'icon': 'fas fa-truck'},
        {'name_ar': 'محامون', 'name_en': 'Law Firms', 'icon': 'fas fa-gavel'},
        {'name_ar': 'محاسبون', 'name_en': 'Accounting', 'icon': 'fas fa-calculator'},
    ]
    
    created_categories = []
    for i, cat_data in enumerate(categories_data):
        category, created = Category.objects.get_or_create(
            slug=f"category-{i+1}",
            defaults={
                'name_ar': cat_data['name_ar'],
                'name_en': cat_data['name_en'],
                'icon': cat_data['icon'],  # الأيقونات مصححة بالفعل مع fas
                'is_active': True,
                'order': (i + 1) * 10,
            }
        )
        if not created:
            # تحديث الأيقونة للتصنيفات الموجودة
            category.icon = cat_data['icon']
            category.save(update_fields=['icon'])
        created_categories.append(category)
    
    print(f"  ✅ تم إنشاء {len(created_categories)} فئة")
    return created_categories



# ... (keep the rest of the functions unchanged: create_businesses, create_products, create_deals, create_reviews, main)
# الكود المتبقي من ملف السكريبت السابق نفسه للدوال create_businesses, create_products, create_deals, create_reviews, main

# ... INSERT REST OF CODE HERE ...
