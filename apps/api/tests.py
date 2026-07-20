"""Regression tests for the mobile API v2 contract."""

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from urllib.parse import parse_qs, urlparse
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


class MobileApiV2AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='mobile-user',
            email='mobile@example.com',
            phone='01000000001',
            password='StrongPass123!',
        )

    def test_login_token_authenticates_profile_request(self):
        login = self.client.post(
            '/api/v2/auth/login/',
            {'username': self.user.username, 'password': 'StrongPass123!'},
            format='json',
        )

        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn('access', login.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        profile = self.client.get('/api/v2/auth/profile/')

        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.data['id'], self.user.id)

    def test_authentication_errors_have_stable_mobile_shape(self):
        response = self.client.get('/api/v2/auth/profile/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['status_code'], 401)
        self.assertIn('errors', response.data)

    def test_logout_blacklists_refresh_token(self):
        login = self.client.post(
            '/api/v2/auth/login/',
            {'username': self.user.username, 'password': 'StrongPass123!'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

        logout = self.client.post(
            '/api/v2/auth/logout/',
            {'refresh': login.data['refresh']},
            format='json',
        )
        self.assertEqual(logout.status_code, status.HTTP_200_OK)

        refresh = self.client.post(
            '/api/v2/auth/refresh/',
            {'refresh': login.data['refresh']},
            format='json',
        )
        self.assertEqual(refresh.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset_changes_password(self):
        request_reset = self.client.post(
            '/api/v2/auth/password-reset/',
            {'email': self.user.email},
            format='json',
        )
        self.assertEqual(request_reset.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

        reset_url = mail.outbox[0].body.splitlines()[2]
        query = parse_qs(urlparse(reset_url).query)
        confirm = self.client.post(
            '/api/v2/auth/password-reset/confirm/',
            {
                'uid': query['uid'][0],
                'token': query['token'][0],
                'password': 'NewStrongPass456!',
                'password_confirm': 'NewStrongPass456!',
            },
            format='json',
        )

        self.assertEqual(confirm.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewStrongPass456!'))

    def test_password_reset_does_not_disclose_unknown_email(self):
        response = self.client.post(
            '/api/v2/auth/password-reset/',
            {'email': 'unknown@example.com'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)


class MobileApiV2RolePermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.regular_user = User.objects.create_user(
            username='regular-user',
            email='regular@example.com',
            phone='01000000002',
            password='StrongPass123!',
        )
        self.business_owner = User.objects.create_user(
            username='business-owner',
            email='owner@example.com',
            phone='01000000003',
            password='StrongPass123!',
            is_business_owner=True,
        )
        self.admin = User.objects.create_superuser(
            username='admin-user',
            email='admin@example.com',
            phone='01000000004',
            password='StrongPass123!',
        )

    def test_regular_user_cannot_access_business_owner_dashboard(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.get('/api/v2/business-owner/dashboard/stats/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_business_owner_can_access_own_dashboard(self):
        self.client.force_authenticate(self.business_owner)
        response = self.client.get('/api/v2/business-owner/dashboard/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_businesses'], 0)

    def test_regular_user_cannot_access_admin_api(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.get('/api/v2/admin/users/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_admin_api(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get('/api/v2/admin/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
