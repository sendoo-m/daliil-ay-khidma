"""Tests for the browser-based dashboard access and location flow."""

from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.directory.models.location import City, Governorate


class OwnerDashboardAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='shop-owner',
            phone='01000000001',
            password='A-strong-password-2026',
        )
        self.client.force_login(self.owner)

    def test_business_create_uses_owner_dashboard_navigation(self):
        response = self.client.get(reverse('dashboard:business_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/base.html')
        self.assertTemplateNotUsed(response, 'dashboard/admin/base.html')
        self.assertContains(response, reverse('dashboard:business_list'))
        self.assertNotContains(response, reverse('dashboard:admin_users_list'))

    def test_login_redirect_setting_targets_dashboard_router(self):
        self.client.logout()
        response = self.client.post(
            reverse('accounts:login'),
            {'username': self.owner.username, 'password': 'A-strong-password-2026'},
        )

        self.assertRedirects(
            response,
            reverse('dashboard:index'),
            fetch_redirect_response=False,
        )


class DashboardLocationAjaxTests(TestCase):
    def setUp(self):
        self.governorate = Governorate.objects.create(
            name_en='Test Governorate',
            name_ar='محافظة اختبار',
        )
        self.active_city = City.objects.create(
            governorate=self.governorate,
            name_en='Active City',
            name_ar='مدينة نشطة',
        )
        City.objects.create(
            governorate=self.governorate,
            name_en='Inactive City',
            name_ar='مدينة غير نشطة',
            is_active=False,
        )

    def test_cities_endpoint_returns_active_cities_for_governorate(self):
        response = self.client.get(
            reverse('dashboard:ajax_cities'),
            {'governorate_id': self.governorate.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'cities': [{'id': self.active_city.pk, 'name_ar': 'مدينة نشطة'}]},
        )

    def test_business_form_uses_named_location_ajax_urls(self):
        owner = User.objects.create_user(
            username='another-owner',
            phone='01000000002',
            password='A-strong-password-2026',
        )
        self.client.force_login(owner)

        response = self.client.get(reverse('dashboard:business_create'))

        self.assertContains(response, reverse('dashboard:ajax_cities'))
        self.assertContains(response, reverse('dashboard:ajax_districts'))
        self.assertNotContains(response, '/dashboard/ajax/get-cities/')
        self.assertNotContains(response, '/dashboard/ajax/get-districts/')
