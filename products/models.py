from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

User = get_user_model()


class MeasuringUnit(models.Model):
    user = models.ForeignKey(User, models.PROTECT, verbose_name='کاربر')
    title = models.CharField(max_length=40, verbose_name='عنوان')

    class Meta:
        verbose_name = 'واحد اندازه گیری'
        verbose_name_plural = 'واحد های اندازه گیری'

    def __str__(self):
        return self.title


class ProductManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Product(models.Model):
    user = models.ForeignKey(User, models.PROTECT, verbose_name='کاربر')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    measuring_unit = models.ForeignKey(MeasuringUnit, models.PROTECT, verbose_name='واحد اندازه گیری')

    objects = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصول ها'

    def __str__(self):
        return self.title
