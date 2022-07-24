from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from products.models import Product

User = get_user_model()


class StoreManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(name__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Store(models.Model):
    user = models.ForeignKey(User, models.PROTECT, verbose_name='کاربر')
    name = models.CharField(max_length=30, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='آخرین تغییر')

    objects = StoreManager()

    class Meta:
        verbose_name = 'انبار'
        verbose_name_plural = 'انبار ها'

    def __str__(self):
        return self.name


class ProductRecordManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(product__title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class ProductRecord(models.Model):
    store = models.ForeignKey(Store, models.CASCADE, verbose_name='انبار')
    product = models.ForeignKey(Product, models.PROTECT, verbose_name='محصول')
    inventory = models.PositiveIntegerField(default=0, verbose_name='موجودی')

    objects = ProductRecordManager()

    class Meta:
        verbose_name = 'موجودی محصول'
        verbose_name_plural = 'موجودی محصول ها'

    def __str__(self):
        return self.product.title
