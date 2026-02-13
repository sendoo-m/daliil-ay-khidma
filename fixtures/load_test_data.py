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
    ismailia_gov, _ = Governorate.objects.get_or_create(
        name_ar='الإسماعيلية',
        defaults={'name_en': 'Ismailia'}
    )
    
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
        city, _ = City.objects.get_or_create(
            governorate=ismailia_gov,
            name_ar=city_data['name_ar'],
            defaults={'name_en': city_data['name_en']}
        )
        for district_data in city_data['districts']:
            district, _ = District.objects.get_or_create(
                city=city,
                name_ar=district_data['name_ar'],
                defaults={'name_en': district_data['name_en']}
            )
            all_districts.append(district)
    
    # ========== محافظة بورسعيد ==========
    portsaid_gov, _ = Governorate.objects.get_or_create(
        name_ar='بورسعيد',
        defaults={'name_en': 'Port Said'}
    )
    
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
        city, _ = City.objects.get_or_create(
            governorate=portsaid_gov,
            name_ar=city_data['name_ar'],
            defaults={'name_en': city_data['name_en']}
        )
        for district_data in city_data['districts']:
            district, _ = District.objects.get_or_create(
                city=city,
                name_ar=district_data['name_ar'],
                defaults={'name_en': district_data['name_en']}
            )
            all_districts.append(district)
    
    # ========== محافظة السويس ==========
    suez_gov, _ = Governorate.objects.get_or_create(
        name_ar='السويس',
        defaults={'name_en': 'Suez'}
    )
    
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
        city, _ = City.objects.get_or_create(
            governorate=suez_gov,
            name_ar=city_data['name_ar'],
            defaults={'name_en': city_data['name_en']}
        )
        for district_data in city_data['districts']:
            district, _ = District.objects.get_or_create(
                city=city,
                name_ar=district_data['name_ar'],
                defaults={'name_en': district_data['name_en']}
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
        created_categories.append(category)
    
    print(f"  ✅ تم إنشاء {len(created_categories)} فئة")
    return created_categories



def create_businesses(owners, districts, categories):
    """إنشاء محلات وأماكن عامة"""
    print("✅ إنشاء المحلات والأماكن العامة...")
    
    # تقسيم التصنيفات
    restaurants_cat = next((c for c in categories if 'مطاعم' in c.name_ar and 'سريعة' not in c.name_ar), categories[0])
    cafes_cat = next((c for c in categories if 'مقاهي' in c.name_ar), categories[1])
    hospitals_cat = next((c for c in categories if 'مستشفيات' in c.name_ar), categories[9])
    parks_cat = next((c for c in categories if 'حدائق' in c.name_ar), categories[32])
    beaches_cat = next((c for c in categories if 'شواطئ' in c.name_ar), categories[33])
    mosques_cat = next((c for c in categories if 'مساجد' in c.name_ar), categories[37])
    churches_cat = next((c for c in categories if 'كنائس' in c.name_ar), categories[38])
    
    businesses_data = [
        # ===== مطاعم ومقاهي =====
        {'name_ar': 'مطعم النافورة', 'name_en': 'Al Nafora Restaurant', 'category': restaurants_cat, 'owner': 0, 'type': 'commercial'},
        {'name_ar': 'كافيه السلام', 'name_en': 'Al Salam Cafe', 'category': cafes_cat, 'owner': 1, 'type': 'commercial'},
        {'name_ar': 'مطعم البحر المتوسط', 'name_en': 'Mediterranean Restaurant', 'category': restaurants_cat, 'owner': 2, 'type': 'commercial'},
        {'name_ar': 'مقهى القناة', 'name_en': 'Canal Cafe', 'category': cafes_cat, 'owner': 3, 'type': 'commercial'},
        {'name_ar': 'مطعم الفيروز', 'name_en': 'Al Fayrouz Restaurant', 'category': restaurants_cat, 'owner': 4, 'type': 'commercial'},
        
        # ===== حدائق عامة =====
        {'name_ar': 'حديقة السلام - الإسماعيلية', 'name_en': 'Al Salam Park - Ismailia', 'category': parks_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'حديقة الأطفال - بورسعيد', 'name_en': 'Children\'s Park - Port Said', 'category': parks_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'حديقة فريال - السويس', 'name_en': 'Ferial Park - Suez', 'category': parks_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'حديقة المسلة - الإسماعيلية', 'name_en': 'Obelisk Park - Ismailia', 'category': parks_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        
        # ===== مستشفيات عامة =====
        {'name_ar': 'مستشفى الإسماعيلية العام', 'name_en': 'Ismailia General Hospital', 'category': hospitals_cat, 'owner': 6, 'type': 'public', 'is_free': False},
        {'name_ar': 'مستشفى بورسعيد العام', 'name_en': 'Port Said General Hospital', 'category': hospitals_cat, 'owner': 6, 'type': 'public', 'is_free': False},
        {'name_ar': 'مستشفى السويس العام', 'name_en': 'Suez General Hospital', 'category': hospitals_cat, 'owner': 6, 'type': 'public', 'is_free': False},
        {'name_ar': 'مستشفى التأمين الصحي - الإسماعيلية', 'name_en': 'Health Insurance Hospital - Ismailia', 'category': hospitals_cat, 'owner': 6, 'type': 'public', 'is_free': False},
        
        # ===== شواطئ =====
        {'name_ar': 'شاطئ فايد العام', 'name_en': 'Fayed Public Beach', 'category': beaches_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'شاطئ بورسعيد الشعبي', 'name_en': 'Port Said Popular Beach', 'category': beaches_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'شاطئ عتاقة - السويس', 'name_en': 'Ataqah Beach - Suez', 'category': beaches_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        
        # ===== مساجد مهمة =====
        {'name_ar': 'مسجد الشهداء - الإسماعيلية', 'name_en': 'Shohada Mosque - Ismailia', 'category': mosques_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'مسجد الفتح - بورسعيد', 'name_en': 'Al Fath Mosque - Port Said', 'category': mosques_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'مسجد أحمد عرابي - السويس', 'name_en': 'Ahmed Orabi Mosque - Suez', 'category': mosques_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'مسجد الإيمان - الإسماعيلية', 'name_en': 'Al Iman Mosque - Ismailia', 'category': mosques_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        
        # ===== كنائس مهمة =====
        {'name_ar': 'كنيسة العذراء مريم - الإسماعيلية', 'name_en': 'Virgin Mary Church - Ismailia', 'category': churches_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'الكنيسة الإنجيلية - بورسعيد', 'name_en': 'Evangelical Church - Port Said', 'category': churches_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        {'name_ar': 'كاتدرائية الأقباط الأرثوذكس - السويس', 'name_en': 'Coptic Orthodox Cathedral - Suez', 'category': churches_cat, 'owner': 5, 'type': 'public', 'is_free': True},
        
        # ===== محلات تجارية متنوعة =====
        {'name_ar': 'محل الأناقة للملابس', 'name_en': 'Elegance Clothing Store', 'category': categories[4], 'owner': 0, 'type': 'commercial'},
        {'name_ar': 'صيدلية النور', 'name_en': 'Al Noor Pharmacy', 'category': categories[11], 'owner': 1, 'type': 'commercial'},
        {'name_ar': 'معرض السيارات الحديثة', 'name_en': 'Modern Cars Showroom', 'category': categories[18], 'owner': 2, 'type': 'commercial'},
        {'name_ar': 'صالون الجمال', 'name_en': 'Beauty Salon', 'category': categories[25], 'owner': 3, 'type': 'commercial'},
        {'name_ar': 'نادي اللياقة الرياضية', 'name_en': 'Fitness Club', 'category': categories[28], 'owner': 4, 'type': 'commercial'},
    ]
    
    created_businesses = []
    for i, bus_data in enumerate(businesses_data):
        district = districts[i % len(districts)]
        owner = owners[bus_data['owner']]
        
        business, created = Business.objects.get_or_create(
            slug=f"business-{i+1}",
            defaults={
                'name_ar': bus_data['name_ar'],
                'name_en': bus_data['name_en'],
                'description_ar': f"وصف {bus_data['name_ar']} - {'مكان عام مفتوح للجميع' if bus_data.get('type') == 'public' else 'نقدم أفضل الخدمات بجودة عالية'}",
                'description_en': f"Description of {bus_data['name_en']} - {'Public place open for everyone' if bus_data.get('type') == 'public' else 'We provide the best services with high quality'}",
                'owner': owner,
                'category': bus_data['category'],
                'district': district,
                'address_ar': f"{district.name_ar}، {district.city.name_ar}",
                'address_en': f"{district.name_en}, {district.city.name_en}",
                'phone': f"+2010{i+1:07d}",
                'email': f"info@business{i+1}.com",
                'website': f"https://business{i+1}.com" if bus_data.get('type') == 'commercial' else '',
                'is_active': True,
                'is_verified': True,
                'is_featured': i < 5,
                'view_count': random.randint(50, 500),
            }
        )
        created_businesses.append(business)
    
    print(f"  ✅ تم إنشاء {len(created_businesses)} محل ومكان عام")
    return created_businesses



def create_products(businesses):
    """إنشاء منتجات وخدمات"""
    print("✅ إنشاء المنتجات...")
    
    products_data = [
        {'name_ar': 'وجبة شاورما', 'name_en': 'Shawarma Meal', 'type': 'product', 'price': 45},
        {'name_ar': 'كابتشينو', 'name_en': 'Cappuccino', 'type': 'product', 'price': 25},
        {'name_ar': 'سمك مشوي', 'name_en': 'Grilled Fish', 'type': 'product', 'price': 120},
        {'name_ar': 'عصير برتقال طازج', 'name_en': 'Fresh Orange Juice', 'type': 'product', 'price': 20},
        {'name_ar': 'بيتزا مارجريتا', 'name_en': 'Margherita Pizza', 'type': 'product', 'price': 80},
        {'name_ar': 'كشري', 'name_en': 'Koshari', 'type': 'product', 'price': 30},
        {'name_ar': 'حلويات شرقية', 'name_en': 'Oriental Sweets', 'type': 'product', 'price': 50},
        {'name_ar': 'قميص قطن', 'name_en': 'Cotton Shirt', 'type': 'product', 'price': 250},
        {'name_ar': 'جلسة مساج', 'name_en': 'Massage Session', 'type': 'service', 'price': 200},
        {'name_ar': 'اشتراك شهري', 'name_en': 'Monthly Subscription', 'type': 'service', 'price': 300},
    ]
    
    created_products = []
    # فقط للمحلات التجارية (نتجنب الأماكن العامة)
    commercial_businesses = [b for b in businesses if 'مسجد' not in b.name_ar and 'كنيسة' not in b.name_ar and 'شاطئ' not in b.name_ar and 'حديقة' not in b.name_ar and 'مستشفى' not in b.name_ar]
    
    for i, prod_data in enumerate(products_data):
        if i >= len(commercial_businesses):
            break
        business = commercial_businesses[i % len(commercial_businesses)]
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
    
    # فقط المحلات التجارية
    commercial_businesses = [b for b in businesses if 'مسجد' not in b.name_ar and 'كنيسة' not in b.name_ar and 'شاطئ' not in b.name_ar and 'حديقة' not in b.name_ar and 'مستشفى' not in b.name_ar]
    
    deals_data = [
        # Active deals
        {'title_ar': 'خصم 50% على جميع الوجبات', 'title_en': '50% Off on All Meals', 'discount': 50, 'start': now - timedelta(days=5), 'end': now + timedelta(days=10)},
        {'title_ar': 'عرض اشتر 2 واحصل على 1 مجاناً', 'title_en': 'Buy 2 Get 1 Free', 'discount': 33, 'start': now - timedelta(days=3), 'end': now + timedelta(days=7)},
        {'title_ar': 'خصم الصيف الكبير', 'title_en': 'Big Summer Sale', 'discount': 40, 'start': now - timedelta(days=2), 'end': now + timedelta(days=20)},
        {'title_ar': 'عرض نهاية الأسبوع', 'title_en': 'Weekend Special', 'discount': 25, 'start': now - timedelta(days=1), 'end': now + timedelta(days=3)},
        
        # Upcoming deals
        {'title_ar': 'عرض العيد الكبير', 'title_en': 'Big Eid Offer', 'discount': 60, 'start': now + timedelta(days=5), 'end': now + timedelta(days=15)},
        {'title_ar': 'خصم العودة للمدارس', 'title_en': 'Back to School Discount', 'discount': 35, 'start': now + timedelta(days=10), 'end': now + timedelta(days=30)},
        
        # Expired deals
        {'title_ar': 'عرض رمضان الكريم', 'title_en': 'Ramadan Offer', 'discount': 30, 'start': now - timedelta(days=40), 'end': now - timedelta(days=5)},
        {'title_ar': 'خصم الشتاء', 'title_en': 'Winter Discount', 'discount': 45, 'start': now - timedelta(days=60), 'end': now - timedelta(days=15)},
    ]
    
    created_deals = []
    for i, deal_data in enumerate(deals_data):
        if i >= len(commercial_businesses):
            break
        business = commercial_businesses[i % len(commercial_businesses)]
        deal, created = Deal.objects.get_or_create(
            slug=f"deal-{i+1}",
            defaults={
                'title_ar': deal_data['title_ar'],
                'title_en': deal_data['title_en'],
                'description_ar': f"وصف {deal_data['title_ar']} - عرض لفترة محدودة لا يفوتك!",
                'description_en': f"Description of {deal_data['title_en']} - Limited time offer don't miss it!",
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
        'تجربة رائعة جداً! أنصح به بشدة',
        'خدمة ممتازة والموظفين محترمين',
        'المكان نظيف والجودة عالية',
        'أسعار معقولة وجودة ممتازة',
        'خدمة جيدة لكن يحتاج تحسين',
        'مكان رائع وأجواء مميزة',
        'سرعة في الخدمة واحترافية',
        'تجربة جيدة بشكل عام',
        'ممتاز ولكن الأسعار مرتفعة قليلاً',
        'مكان مريح ونظيف جداً',
    ]
    
    created_reviews = []
    review_count = 0
    
    # اختيار بعض المحلات للتقييم
    for business in businesses[:10]:
        num_reviews = random.randint(3, 6)
        for i in range(num_reviews):
            if review_count >= len(customers):
                break
            
            customer = customers[review_count % len(customers)]
            rating = random.choice([5, 5, 4, 4, 4, 3])
            
            review, created = Review.objects.get_or_create(
                business=business,
                user=customer,
                defaults={
                    'rating': rating,
                    'comment': comments[review_count % len(comments)],
                    'is_approved': True,
                }
            )
            
            # رد على بعض التقييمات
            if random.choice([True, False]):
                ReviewReply.objects.get_or_create(
                    review=review,
                    defaults={
                        'user': business.owner,
                        'comment': 'شكراً جزيلاً لتقييمك، نسعى دائماً لتقديم الأفضل!',
                    }
                )
            
            created_reviews.append(review)
            review_count += 1
    
    print(f"  ✅ تم إنشاء {len(created_reviews)} تقييم")
    return created_reviews



def main():
    """الدالة الرئيسية"""
    print("✨ بدء تحميل البيانات التجريبية الموسعة...\n")
    
    # Create data
    owners, customers = create_users()
    districts = create_locations()
    categories = create_categories()
    businesses = create_businesses(owners, districts, categories)
    products = create_products(businesses)
    deals = create_deals(businesses)
    reviews = create_reviews(businesses, customers)
    
    print("\n" + "="*60)
    print("✨ تم تحميل جميع البيانات بنجاح!")
    print("="*60)
    
    print("\n📊 إحصائيات البيانات:")
    print(f"  - المستخدمين: {len(owners)} أصحاب محلات + {len(customers)} عميل")
    print(f"  - المحافظات: 3 (الإسماعيلية، بورسعيد، السويس)")
    print(f"  - الأحياء: {len(districts)}")
    print(f"  - التصنيفات: {len(categories)}")
    print(f"  - المحلات والأماكن: {len(businesses)}")
    print(f"  - المنتجات: {len(products)}")
    print(f"  - العروض: {len(deals)}")
    print(f"  - التقييمات: {len(reviews)}")
    
    print("\n🔑 بيانات الدخول:")
    print("  - المستخدم: ahmed_owner")
    print("  - كلمة المرور: test123")
    print("\n  أو استخدم:")
    print("  - fatima_owner / khaled_owner / maha_owner / omar_owner")
    print("  - كلمة المرور: test123")
    
    print("\n🎯 أماكن عامة تم إضافتها:")
    print("  ✅ حدائق في المحافظات الثلاث")
    print("  ✅ مستشفيات عامة")
    print("  ✅ شواطئ عامة (فايد، بورسعيد، عتاقة)")
    print("  ✅ مساجد مهمة")
    print("  ✅ كنائس مهمة")
    
    print("\n🚀 يمكنك الآن الدخول واختبار المنصة!")
    print("="*60 + "\n")



if __name__ == '__main__':
    main()
