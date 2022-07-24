from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from products.models import MeasuringUnit, Product
from settings.models import SiteSettings

User = get_user_model()


class MeasuringTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.settings = SiteSettings.objects.create(
            title='settings',
            site_url='www.example.com',
            short_des='storage manager',
            email='test@test.com',
            about_us='We manage your storage.',
            copy_right='copy right text',
            logo_image='log-image.jpg',
            fav_icon='fav-icon.fav',
        )
        self.measuring_unit = MeasuringUnit.objects.create(
            user=self.user,
            title='measuring unit',
        )
        self.product = Product.objects.create(
            user=self.user,
            title='product',
            measuring_unit=self.measuring_unit,
        )

    def test_measuring_unit_listing(self):
        self.assertEqual(self.measuring_unit.user, self.user)
        self.assertEqual(self.measuring_unit.title, 'measuring unit')

    def test_product_listing(self):
        self.assertEqual(self.product.user, self.user)
        self.assertEqual(self.product.title, 'product')
        self.assertEqual(self.product.measuring_unit, self.measuring_unit)

    def test_measuring_units_list_view(self):
        response = self.client.get(reverse('measuring-units'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'measuring unit')
        self.assertNotContains(response, 'Hello, I should not be on the page.')
        self.assertTemplateUsed('measuring_unit/measuring_units.html')

    def test_products_list_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product')
        self.assertNotContains(response, 'hello')
        self.assertTemplateUsed(response, 'product/products.html')
