"""Create a complete, repeatable demo dataset for design and journey testing."""

from datetime import time, timedelta
from decimal import Decimal
from xml.sax.saxutils import escape

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.categories.models import Category
from apps.deals.models import Deal, DealClaim
from apps.directory.models import (
    Business,
    BusinessImage,
    BusinessWorkingHours,
    City,
    District,
    Favorite,
    Governorate,
)
from apps.notifications.models import Notification
from apps.products.models import Product, ProductImage
from apps.reviews.models import Review, ReviewLike, ReviewReply, ReviewReport
from apps.subscriptions.models import Subscription, SubscriptionPlan

DEMO_PREFIX = "demo_"
DEMO_SLUG_PREFIX = "demo-"
DEMO_PASSWORD = "Demo@12345"


class Command(BaseCommand):
    help = "إنشاء داتا تجريبية شاملة، أو حذف الداتا التجريبية فقط"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="حذف الداتا التجريبية فقط دون إنشاء بيانات جديدة",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="حذف الداتا التجريبية ثم إعادة إنشائها من البداية",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"] or options["reset"]:
            self._clear_demo_data()
            if options["clear"]:
                self.stdout.write(self.style.SUCCESS("تم حذف الداتا التجريبية فقط."))
                return

        if self._demo_exists():
            self.stdout.write(
                self.style.WARNING(
                    "الداتا التجريبية موجودة بالفعل؛ لم يتم تكرارها. "
                    "استخدم --reset لإعادة إنشائها."
                )
            )
            self._print_summary()
            return

        self.stdout.write("جاري إنشاء الداتا التجريبية الشاملة...")
        owners, customers = self._create_users()
        districts = self._create_locations()
        categories = self._create_categories()
        businesses = self._create_businesses(owners, districts, categories)
        self._create_working_hours(businesses)
        products = self._create_products(businesses)
        deals = self._create_deals(businesses)
        self._create_reviews_and_activity(businesses, customers, deals)
        self._create_subscriptions(businesses)
        self._create_notifications(owners, customers, businesses, deals)
        self._add_images(categories, businesses, products, deals)

        self.stdout.write(self.style.SUCCESS("تم إنشاء الداتا التجريبية بنجاح."))
        self.stdout.write(f"كلمة مرور جميع الحسابات التجريبية: {DEMO_PASSWORD}")
        self._print_summary()

    def _demo_exists(self):
        return (
            get_user_model().objects.filter(username__startswith=DEMO_PREFIX).exists()
        )

    def _clear_demo_data(self):
        self.stdout.write("جاري حذف الداتا التجريبية فقط...")
        get_user_model().objects.filter(username__startswith=DEMO_PREFIX).delete()
        Business.objects.filter(slug__startswith=DEMO_SLUG_PREFIX).delete()
        Category.objects.filter(slug__startswith=DEMO_SLUG_PREFIX).delete()
        District.objects.filter(slug__startswith=DEMO_SLUG_PREFIX).delete()
        City.objects.filter(slug__startswith=DEMO_SLUG_PREFIX).delete()
        Governorate.objects.filter(slug__startswith=DEMO_SLUG_PREFIX).delete()
        SubscriptionPlan.objects.filter(name__startswith="demo_").delete()

    def _create_users(self):
        User = get_user_model()
        owner_names = [
            ("ahmed", "أحمد", "الطبيب"),
            ("mahmoud", "محمود", "الكهربائي"),
            ("youssef", "يوسف", "الحلاق"),
            ("nour", "نور", "المصممة"),
            ("mariam", "مريم", "صاحبة المتجر"),
            ("karim", "كريم", "مقدم الخدمة"),
        ]
        customer_names = [
            ("sara", "سارة", "محمد"),
            ("omar", "عمر", "علي"),
            ("layla", "ليلى", "حسن"),
            ("tarek", "طارق", "سعيد"),
            ("huda", "هدى", "خالد"),
        ]
        owners, customers = [], []
        for index, (key, first, last) in enumerate(owner_names, 1):
            user = User.objects.create_user(
                username=f"{DEMO_PREFIX}owner_{key}",
                password=DEMO_PASSWORD,
                email=f"demo.owner.{key}@example.com",
                phone=f"0109000{index:04d}",
                first_name=first,
                last_name=last,
                city="الإسماعيلية",
                is_business_owner=True,
                email_verified=True,
            )
            owners.append(user)
        for index, (key, first, last) in enumerate(customer_names, 101):
            user = User.objects.create_user(
                username=f"{DEMO_PREFIX}customer_{key}",
                password=DEMO_PASSWORD,
                email=f"demo.customer.{key}@example.com",
                phone=f"0119000{index:04d}",
                first_name=first,
                last_name=last,
                city="الإسماعيلية",
                email_verified=index % 2 == 1,
            )
            customers.append(user)
        return owners, customers

    def _create_locations(self):
        data = [
            (
                "Ismailia",
                "الإسماعيلية",
                [
                    (
                        "Ismailia",
                        "الإسماعيلية",
                        [
                            ("Sheikh Zayed", "الشيخ زايد"),
                            ("Al Salam", "حي السلام"),
                            ("Downtown", "وسط البلد"),
                        ],
                    )
                ],
            ),
            (
                "Cairo",
                "القاهرة",
                [
                    (
                        "Cairo",
                        "القاهرة",
                        [("Nasr City", "مدينة نصر"), ("Maadi", "المعادي")],
                    )
                ],
            ),
            (
                "Suez",
                "السويس",
                [
                    (
                        "Suez",
                        "السويس",
                        [("Faisal", "حي فيصل"), ("Arbaeen", "حي الأربعين")],
                    )
                ],
            ),
        ]
        districts = []
        for gov_order, (gov_en, gov_ar, cities) in enumerate(data, 1):
            gov = Governorate.objects.create(
                name_en=f"Demo {gov_en}",
                name_ar=f"{gov_ar} (تجريبي)",
                slug=f"{DEMO_SLUG_PREFIX}{gov_en.lower()}",
                order=gov_order,
            )
            for city_order, (city_en, city_ar, areas) in enumerate(cities, 1):
                city = City.objects.create(
                    governorate=gov,
                    name_en=f"Demo {city_en}",
                    name_ar=f"{city_ar} (تجريبي)",
                    slug=f"{DEMO_SLUG_PREFIX}{gov_en.lower()}-{city_en.lower().replace(' ', '-')}",
                    order=city_order,
                )
                for area_order, (area_en, area_ar) in enumerate(areas, 1):
                    districts.append(
                        District.objects.create(
                            city=city,
                            name_en=f"Demo {area_en}",
                            name_ar=f"{area_ar} (تجريبي)",
                            slug=(f"{DEMO_SLUG_PREFIX}{gov_en}-{city_en}-{area_en}")
                            .lower()
                            .replace(" ", "-"),
                            order=area_order,
                        )
                    )
        return districts

    def _create_categories(self):
        data = [
            ("medical", "Medical Services", "الخدمات الطبية", "fas fa-stethoscope"),
            ("crafts", "Home Services", "الخدمات المنزلية والحرفية", "fas fa-tools"),
            ("beauty", "Beauty", "الجمال والعناية", "fas fa-cut"),
            ("creative", "Creative Services", "الخدمات الإبداعية", "fas fa-palette"),
            ("shopping", "Shopping", "التسوق", "fas fa-store"),
            ("food", "Food and Cafes", "المطاعم والمقاهي", "fas fa-utensils"),
        ]
        categories = {}
        for order, (key, en, ar, icon) in enumerate(data, 1):
            parent = Category.objects.create(
                name_en=f"Demo {en}",
                name_ar=f"{ar} (تجريبي)",
                slug=f"{DEMO_SLUG_PREFIX}{key}",
                icon=icon,
                order=order,
                description_ar=f"قسم تجريبي شامل لاختبار صفحات {ar}.",
                description_en=f"Demo category for testing {en} pages.",
            )
            categories[key] = parent
        return categories

    def _create_businesses(self, owners, districts, categories):
        data = [
            (
                "doctor",
                "عيادة د. أحمد للقلب",
                "Dr Ahmed Cardiology Clinic",
                "public",
                "medical",
            ),
            (
                "electrician",
                "محمود للكهرباء المنزلية",
                "Mahmoud Home Electrician",
                "craft",
                "crafts",
            ),
            ("barber", "صالون يوسف للرجال", "Youssef Men's Salon", "shop", "beauty"),
            (
                "designer",
                "استوديو نور للتصميم",
                "Nour Design Studio",
                "craft",
                "creative",
            ),
            ("store", "بيت الهدايا", "Gift House", "shop", "shopping"),
            ("cafe", "كافيه المرسى", "Al Marsa Cafe", "shop", "food"),
        ]
        businesses = []
        for index, (key, ar, en, business_type, category_key) in enumerate(data):
            business = Business.objects.create(
                owner=owners[index],
                business_type=business_type,
                name_en=en,
                name_ar=ar,
                slug=f"{DEMO_SLUG_PREFIX}{key}",
                category=categories[category_key],
                district=districts[index % len(districts)],
                phone=f"0128000{index + 1:04d}",
                whatsapp=f"0128000{index + 1:04d}",
                email=f"{key}.demo@example.com",
                website="https://example.com",
                facebook="https://facebook.com/example",
                instagram="https://instagram.com/example",
                address_en="Main street, beside the public square",
                address_ar="الشارع الرئيسي، بجوار الميدان العام",
                description_en=f"A complete demo profile for {en}, with realistic services and contact details.",
                description_ar=f"ملف تجريبي متكامل لـ {ar} يضم خدمات وبيانات تواصل واقعية للاختبار.",
                working_hours_en="Saturday–Thursday: 9 AM–9 PM",
                working_hours_ar="السبت–الخميس: 9 صباحًا–9 مساءً",
                latitude=Decimal("30.590000") + Decimal(index) / 100,
                longitude=Decimal("32.270000") + Decimal(index) / 100,
                is_active=index != 5,
                is_verified=index != 4,
                is_featured=index in (0, 2, 3),
                is_promoted=index in (1, 3),
                view_count=1250 - index * 137,
                click_count=280 - index * 23,
            )
            businesses.append(business)
        return businesses

    def _create_working_hours(self, businesses):
        for business in businesses:
            for day in range(7):
                BusinessWorkingHours.objects.create(
                    business=business,
                    day=day,
                    opening_time=None if day == 5 else time(9),
                    closing_time=None if day == 5 else time(21),
                    is_closed=day == 5,
                )

    def _create_products(self, businesses):
        catalog = {
            "doctor": [
                ("كشف طبي", "Medical examination", "service", 450),
                ("استشارة متابعة", "Follow-up", "service", 250),
            ],
            "electrician": [
                ("زيارة وفحص أعطال", "Inspection visit", "service", 200),
                ("تركيب لوحة كهرباء", "Panel installation", "service", 1200),
            ],
            "barber": [
                ("قص شعر وتصفيف", "Haircut", "service", 180),
                ("باقة العريس", "Groom package", "service", 900),
            ],
            "designer": [
                ("تصميم هوية بصرية", "Brand identity", "service", 3500),
                ("تصميم منشورات", "Social posts", "service", 800),
            ],
            "store": [
                ("صندوق هدايا", "Gift box", "product", 650),
                ("كوب مخصص", "Custom mug", "product", 220),
            ],
            "cafe": [
                ("قهوة مختصة", "Specialty coffee", "product", 85),
                ("إفطار المرسى", "Marsa breakfast", "product", 240),
            ],
        }
        products = []
        for business in businesses:
            key = business.slug.removeprefix(DEMO_SLUG_PREFIX)
            for order, (ar, en, product_type, price) in enumerate(catalog[key], 1):
                products.append(
                    Product.objects.create(
                        business=business,
                        name_ar=ar,
                        name_en=en,
                        slug=f"{business.slug}-{order}",
                        product_type=product_type,
                        description_ar=f"وصف تجريبي مفصل لخدمة أو منتج {ar}.",
                        description_en=f"Detailed demo description for {en}.",
                        price=Decimal(price),
                        old_price=(
                            Decimal(price) * Decimal("1.20") if order == 1 else None
                        ),
                        is_available=not (business.slug == "demo-store" and order == 2),
                        stock_quantity=25 if product_type == "product" else None,
                        has_delivery=product_type == "product",
                        delivery_cost=35 if product_type == "product" else None,
                        delivery_time_ar="خلال يومين",
                        delivery_time_en="Within two days",
                        order=order,
                        is_featured=order == 1,
                        view_count=240 - order * 35,
                    )
                )
        return products

    def _create_deals(self, businesses):
        now = timezone.now()
        specs = [
            (
                businesses[2],
                "خصم 25% على باقة العريس",
                "25% off groom package",
                now - timedelta(days=3),
                now + timedelta(days=20),
                True,
            ),
            (
                businesses[4],
                "هدية مجانية مع كل طلب",
                "Free gift with every order",
                now + timedelta(days=5),
                now + timedelta(days=30),
                False,
            ),
            (
                businesses[5],
                "عرض الإفطار لشخصين",
                "Breakfast for two",
                now - timedelta(days=30),
                now - timedelta(days=2),
                False,
            ),
        ]
        deals = []
        for index, (business, ar, en, start, end, featured) in enumerate(specs, 1):
            deals.append(
                Deal.objects.create(
                    business=business,
                    title_ar=ar,
                    title_en=en,
                    slug=f"{DEMO_SLUG_PREFIX}deal-{index}",
                    description_ar=f"تفاصيل وشروط العرض التجريبي: {ar}.",
                    description_en=f"Demo offer details and terms: {en}.",
                    deal_type="percentage" if index == 1 else "special",
                    discount_percentage=25 if index == 1 else None,
                    original_price=900 if index == 1 else None,
                    final_price=675 if index == 1 else None,
                    start_date=start,
                    end_date=end,
                    terms_ar="للاستخدام مرة واحدة.",
                    terms_en="One use per customer.",
                    max_uses=100,
                    max_uses_per_user=1,
                    is_featured=featured,
                    view_count=480 - index * 70,
                )
            )
        return deals

    def _create_reviews_and_activity(self, businesses, customers, deals):
        comments = [
            "خدمة ممتازة والتزام بالموعد.",
            "تجربة جيدة وسأكررها.",
            "جودة رائعة وتعامل محترم.",
            "السعر مناسب والنتيجة مرضية.",
            "أنصح بالتجربة.",
        ]
        reviews = []
        for business_index, business in enumerate(businesses[:5]):
            for customer_index, customer in enumerate(customers[:3]):
                review = Review.objects.create(
                    business=business,
                    user=customer,
                    rating=5 - ((business_index + customer_index) % 3),
                    comment=comments[(business_index + customer_index) % len(comments)],
                    is_approved=not (business_index == 4 and customer_index == 2),
                )
                reviews.append(review)
                if customer_index == 0:
                    ReviewReply.objects.create(
                        review=review,
                        user=business.owner,
                        comment="شكرًا لتقييمك، نسعد بخدمتك دائمًا.",
                    )
        for index, review in enumerate(reviews[:5]):
            ReviewLike.objects.create(
                review=review, user=customers[(index + 1) % len(customers)]
            )
        ReviewReport.objects.create(
            review=reviews[-1],
            user=customers[4],
            reason="بلاغ تجريبي لاختبار رحلة المراجعة الإدارية.",
        )
        for index, business in enumerate(businesses[:4]):
            Favorite.objects.create(user=customers[index], business=business)
        for index, deal in enumerate(deals[:2]):
            DealClaim.objects.create(
                deal=deal,
                user=customers[index],
                is_used=index == 0,
                used_at=timezone.now() if index == 0 else None,
                notes="مطالبة تجريبية",
            )
            Deal.objects.filter(pk=deal.pk).update(current_uses=1)

    def _create_subscriptions(self, businesses):
        now = timezone.now()
        plan_specs = [
            ("demo_free", "Demo Free", "تجريبي مجاني", 0, 0, False),
            ("demo_basic", "Demo Basic", "تجريبي أساسي", 199, 10, False),
            ("demo_premium", "Demo Premium", "تجريبي مميز", 399, 30, True),
            ("demo_vip", "Demo VIP", "تجريبي نخبة", 699, 0, True),
        ]
        plans = []
        for order, (name, en, ar, price, max_products, popular) in enumerate(
            plan_specs
        ):
            plans.append(
                SubscriptionPlan.objects.create(
                    name=name,
                    display_name_en=en,
                    display_name_ar=ar,
                    description_ar="خطة تجريبية لاختبار الاشتراكات والصلاحيات.",
                    description_en="Demo plan for subscription and permissions testing.",
                    price_monthly=price,
                    price_quarterly=price * 3,
                    price_semi_annual=price * 6,
                    price_annual=price * 12,
                    max_products=max_products,
                    max_images_per_product=5,
                    max_business_images=10,
                    can_upload_images=name != "demo_free",
                    can_show_prices=name != "demo_free",
                    has_delivery_options=name in ("demo_premium", "demo_vip"),
                    has_analytics=name in ("demo_premium", "demo_vip"),
                    featured_in_search=name == "demo_vip",
                    can_create_deals=name in ("demo_premium", "demo_vip"),
                    has_verified_badge=name == "demo_vip",
                    order=order,
                    is_popular=popular,
                )
            )
        for index, business in enumerate(businesses):
            plan = plans[index % len(plans)]
            status = "expired" if index == 5 else "active"
            Subscription.objects.create(
                business=business,
                plan=plan,
                start_date=now - timedelta(days=20),
                end_date=(
                    now - timedelta(days=1)
                    if status == "expired"
                    else now + timedelta(days=40 + index)
                ),
                status=status,
                auto_renew=index % 2 == 0,
                amount_paid=plan.price_monthly,
                payment_method="Demo card",
                transaction_id=f"DEMO-TXN-{index + 1:03d}",
            )

    def _create_notifications(self, owners, customers, businesses, deals):
        users = owners[:3] + customers[:3]
        for index, user in enumerate(users):
            Notification.objects.create(
                user=user,
                notification_type=["business", "deal", "review"][index % 3],
                title_ar="إشعار تجريبي جديد",
                title_en="New demo notification",
                body_ar="هذا إشعار لاختبار شاشة الإشعارات وحالة القراءة.",
                body_en="This notification tests the list and read state.",
                data={
                    "demo": True,
                    "business_slug": businesses[index % len(businesses)].slug,
                },
                is_read=index % 2 == 0,
                read_at=timezone.now() if index % 2 == 0 else None,
            )

    def _svg(self, title, color, width=1200, height=600):
        title = escape(title)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs><linearGradient id="g"><stop stop-color="{color}"/><stop offset="1" stop-color="#111827"/></linearGradient></defs>
<rect width="100%" height="100%" fill="url(#g)"/><circle cx="{width * .82}" cy="{height * .2}" r="{height * .28}" fill="#fff" opacity=".12"/>
<text x="50%" y="48%" fill="white" font-size="{max(28, height // 11)}" font-family="Arial" text-anchor="middle">{title}</text>
<text x="50%" y="62%" fill="white" opacity=".8" font-size="{max(18, height // 22)}" font-family="Arial" text-anchor="middle">Daliil Ay Khidma • Demo</text></svg>"""
        return ContentFile(svg.encode("utf-8"))

    def _add_images(self, categories, businesses, products, deals):
        colors = ["#0f766e", "#2563eb", "#7c3aed", "#db2777", "#ea580c", "#0891b2"]
        for index, category in enumerate(categories.values()):
            category.image.save(
                f"{category.slug}.svg",
                self._svg(category.name_en, colors[index], 800, 500),
                save=True,
            )
        for index, business in enumerate(businesses):
            color = colors[index % len(colors)]
            business.logo.save(
                f"{business.slug}-logo.svg",
                self._svg(business.name_en, color, 500, 500),
                save=False,
            )
            business.cover_image.save(
                f"{business.slug}-cover.svg",
                self._svg(business.name_en, color),
                save=True,
            )
            for image_order in range(2):
                image = BusinessImage(
                    business=business,
                    caption_ar="صورة تجريبية من معرض الأعمال",
                    caption_en="Demo gallery image",
                    order=image_order,
                )
                image.image.save(
                    f"{business.slug}-gallery-{image_order + 1}.svg",
                    self._svg(f"{business.name_en} Gallery {image_order + 1}", color),
                    save=True,
                )
        for index, product in enumerate(products):
            image = ProductImage(
                product=product,
                alt_text_ar=product.name_ar,
                alt_text_en=product.name_en,
                is_primary=True,
            )
            image.image.save(
                f"{product.slug}.svg",
                self._svg(product.name_en, colors[index % len(colors)], 800, 600),
                save=True,
            )
        for index, deal in enumerate(deals):
            deal.image.save(
                f"{deal.slug}.svg",
                self._svg(deal.title_en, colors[index % len(colors)]),
                save=True,
            )

    def _print_summary(self):
        counts = {
            "الحسابات": get_user_model()
            .objects.filter(username__startswith=DEMO_PREFIX)
            .count(),
            "الأنشطة": Business.objects.filter(
                slug__startswith=DEMO_SLUG_PREFIX
            ).count(),
            "المنتجات والخدمات": Product.objects.filter(
                slug__startswith=DEMO_SLUG_PREFIX
            ).count(),
            "العروض": Deal.objects.filter(
                slug__startswith=f"{DEMO_SLUG_PREFIX}deal-"
            ).count(),
            "التقييمات": Review.objects.filter(
                business__slug__startswith=DEMO_SLUG_PREFIX
            ).count(),
            "الإشعارات": Notification.objects.filter(
                user__username__startswith=DEMO_PREFIX
            ).count(),
        }
        self.stdout.write(
            "ملخص الداتا: "
            + "، ".join(f"{name}: {count}" for name, count in counts.items())
        )
