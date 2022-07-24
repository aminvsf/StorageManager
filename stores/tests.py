from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from settings.models import SiteSettings
from products.models import Product, MeasuringUnit

from .models import Store, ProductRecord

User = get_user_model()


class StoresTest(TestCase):
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
        self.store = Store.objects.create(
            user=self.user,
            name='store one',
        )
        self.measuring_unit = MeasuringUnit.objects.create(
            user=self.user,
            title='measuring_unit',
        )
        self.product = Product.objects.create(
            user=self.user,
            title='product',
            measuring_unit=self.measuring_unit,
        )
        self.product_record = ProductRecord.objects.create(
            store=self.store,
            product=self.product,
            inventory=100,
        )

    def test_store_listing(self):
        self.assertEqual(self.store.user, self.user)
        self.assertEqual(self.store.name, 'store one')

    def test_product_record_listing(self):
        self.assertEqual(self.product_record.store, self.store)
        self.assertEqual(self.product_record.product, self.product)
        self.assertEqual(self.product_record.inventory, 100)

    def test_store_list_view(self):
        response = self.client.get(reverse('stores'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'store one')
        self.assertNotContains(response, 'hello')
        self.assertTemplateUsed(response, 'store/stores.html')

    def test_store_detail_view(self):
        response = self.client.get(reverse('stores-detail', kwargs={'pk': self.store.id}))
        no_response = self.client.get(reverse('stores-detail', kwargs={'pk': 12345}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'store one')
        self.assertContains(response, 'product')
        self.assertNotContains(response, 'hello')
        self.assertTemplateUsed(response, 'store/stores_detail.html')
