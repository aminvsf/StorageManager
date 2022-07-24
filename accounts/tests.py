from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):
    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username='test_user',
            email='testuser@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(
            username='admin_user',
            email='adminuser@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'admin_user')
        self.assertEqual(admin_user.email, 'adminuser@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
