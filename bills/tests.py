from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from products.models import MeasuringUnit, Product
from settings.models import SiteSettings
from stores.models import Store
from .models import Input, InputDetail, Output, OutputDetail

User = get_user_model()


class BillsTest(TestCase):
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
        self.input = Input.objects.create(
            store=self.store,
            title='input',
        )
        self.output = Output.objects.create(
            store=self.store,
            cause='output',
        )
        self.measuring_unit = MeasuringUnit.objects.create(
            user=self.user,
            title='measuring_unit',
        )
        self.product_first = Product.objects.create(
            user=self.user,
            title='product_first',
            measuring_unit=self.measuring_unit,
        )
        self.product_second = Product.objects.create(
            user=self.user,
            title='product_second',
            measuring_unit=self.measuring_unit,
        )

    def test_input_listing(self):
        self.assertEqual(self.input.store, self.store)
        self.assertEqual(self.input.title, 'input')

    def test_output_listing(self):
        self.assertEqual(self.output.store, self.store)
        self.assertEqual(self.output.cause, 'output')

    def test_input_list_view(self):
        response = self.client.get(reverse('inputs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'input')
        self.assertNotContains(response, 'hello')
        self.assertTemplateUsed(response, 'bill/inputs.html')

    def test_output_list_view(self):
        response = self.client.get(reverse('outputs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'output')
        self.assertNotContains(response, 'hello')
        self.assertTemplateUsed(response, 'bill/outputs.html')

    def test_input_detail_view(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=50,
        )
        response = self.client.get(reverse('inputs-detail', kwargs={'pk': self.input.id}))
        no_response = self.client.get(reverse('inputs-detail', kwargs={'pk': 12345}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'input')
        self.assertContains(response, 'product_first')
        self.assertContains(response, '50')
        self.assertNotContains(response, 'hello')
        self.assertTemplateUsed(response, 'bill/inputs_detail.html')

    def test_output_detail_view(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_second,
            input=self.input,
            value=50,
        )
        self.output_detail = OutputDetail.objects.create(
            product=self.product_second,
            output=self.output,
            value=0,
        )
        self.output_detail.value += 25
        self.output_detail.save()
        response = self.client.get(reverse('outputs-detail', kwargs={'pk': self.output.id}))
        no_response = self.client.get(reverse('outputs-detail', kwargs={'pk': 12345}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'output')
        self.assertContains(response, 'product_second')
        self.assertContains(response, '25')
        self.assertNotContains(response, 'hello')
        self.assertTemplateUsed(response, 'bill/outputs_detail.html')

    def test_input_detail_creation(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 150)

    def test_input_detail_increase(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.input_detail.value += 50
        self.input_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 200)

    def test_input_detail_decrease(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.input_detail.value -= 100
        self.input_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 50)

    def test_input_detail_product_change(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 150)
        self.assertIsNone(self.store.productrecord_set.filter(product=self.product_second).first())
        self.input_detail.product = self.product_second
        self.input_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_second).first().inventory, 150)
        self.assertIsNone(self.store.productrecord_set.filter(product=self.product_first).first())

    def test_input_detail_product_and_value_change(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 150)
        self.assertIsNone(self.store.productrecord_set.filter(product=self.product_second).first())
        self.input_detail.product = self.product_second
        self.input_detail.value += 50
        self.input_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_second).first().inventory, 200)
        self.assertIsNone(self.store.productrecord_set.filter(product=self.product_first).first())

    def test_input_detail_delete(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 150)
        self.input_detail.delete()
        self.assertIsNone(self.store.productrecord_set.filter(product=self.product_first).first())

    def test_output_detail_creation(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.output_detail = OutputDetail.objects.create(
            product=self.product_first,
            output=self.output,
            value=0,
        )
        self.output_detail.value += 50
        self.output_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 100)

    def test_output_detail_decrease(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.output_detail = OutputDetail.objects.create(
            product=self.product_first,
            output=self.output,
            value=0,
        )
        self.output_detail.value += 50
        self.output_detail.save()
        self.output_detail.value -= 25
        self.output_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 125)

    def test_output_detail_product_change(self):
        self.input_detail_first = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.input_detail_second = InputDetail.objects.create(
            product=self.product_second,
            input=self.input,
            value=300,
        )
        self.output_detail = OutputDetail.objects.create(
            product=self.product_first,
            output=self.output,
            value=0,
        )
        self.output_detail.value += 50
        self.output_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 100)
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_second).first().inventory, 300)
        self.output_detail.product = self.product_second
        self.output_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 150)
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_second).first().inventory, 250)

    def test_output_detail_product_and_value_change(self):
        self.input_detail_first = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=200,
        )
        self.input_detail_second = InputDetail.objects.create(
            product=self.product_second,
            input=self.input,
            value=400,
        )
        self.output_detail = OutputDetail.objects.create(
            product=self.product_first,
            output=self.output,
            value=0,
        )
        self.output_detail.value += 50
        self.output_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 150)
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_second).first().inventory, 400)
        self.output_detail.product = self.product_second
        self.output_detail.value += 25
        self.output_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 200)
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_second).first().inventory, 325)

    def test_output_detail_delete(self):
        self.input_detail = InputDetail.objects.create(
            product=self.product_first,
            input=self.input,
            value=150,
        )
        self.output_detail = OutputDetail.objects.create(
            product=self.product_first,
            output=self.output,
            value=0,
        )
        self.output_detail.value += 50
        self.output_detail.save()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 100)
        self.output_detail.delete()
        self.assertEqual(self.store.productrecord_set.filter(product=self.product_first).first().inventory, 150)
