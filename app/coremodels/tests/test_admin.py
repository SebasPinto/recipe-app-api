from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.apps import apps


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password123',
            name='Test User Full Name'
        )

    def test_users_listed(self):
        """
        Tests the users are listed on user page
        """
        app_label = 'coremodels'
        model = 'user'
        url = reverse(f'admin:{app_label}_{model}_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test that user edit page works
        """
        url = reverse(f'admin:coremodels_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """
        Test that the create user page works
        """
        url = reverse('admin:coremodels_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
