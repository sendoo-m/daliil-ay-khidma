from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.categories.models import Category
from apps.deals.models import Deal
from apps.directory.models import Business
from apps.notifications.models import Notification
from apps.products.models import Product
from apps.reviews.models import Review
from apps.subscriptions.models import Subscription


class SeedDemoDataCommandTests(TestCase):
    def test_seed_is_comprehensive_and_idempotent(self):
        output = StringIO()
        call_command("seed_demo_data", stdout=output)

        self.assertEqual(
            get_user_model().objects.filter(username__startswith="demo_").count(), 11
        )
        self.assertEqual(Business.objects.filter(slug__startswith="demo-").count(), 6)
        self.assertEqual(Product.objects.filter(slug__startswith="demo-").count(), 12)
        self.assertEqual(Deal.objects.filter(slug__startswith="demo-deal-").count(), 3)
        self.assertEqual(
            Review.objects.filter(business__slug__startswith="demo-").count(), 15
        )
        self.assertEqual(
            Subscription.objects.filter(business__slug__startswith="demo-").count(), 6
        )
        self.assertEqual(
            Notification.objects.filter(user__username__startswith="demo_").count(), 6
        )
        self.assertTrue(
            Business.objects.filter(
                logo__endswith=".svg", cover_image__endswith=".svg"
            ).exists()
        )

        call_command("seed_demo_data", stdout=output)
        self.assertEqual(Business.objects.filter(slug__startswith="demo-").count(), 6)
        self.assertIn("موجودة بالفعل", output.getvalue())

    def test_clear_removes_only_demo_data(self):
        real_category = Category.objects.create(
            name_en="Real", name_ar="حقيقي", slug="real"
        )
        call_command("seed_demo_data", stdout=StringIO())
        call_command("seed_demo_data", "--clear", stdout=StringIO())

        self.assertFalse(
            get_user_model().objects.filter(username__startswith="demo_").exists()
        )
        self.assertFalse(Business.objects.filter(slug__startswith="demo-").exists())
        self.assertTrue(Category.objects.filter(pk=real_category.pk).exists())
