from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models import Q

from config.DateTimeRelated.DateTimeFormatter import timestamp_formatter
from products.models import Product
from stores.models import Store, ProductRecord


class InputManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(title__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Input(models.Model):
    store = models.ForeignKey(Store, models.CASCADE, verbose_name='انبار')
    title = models.CharField(max_length=300, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='تاریخ و زمان')

    objects = InputManager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'حواله ورود'
        verbose_name_plural = 'حواله های ورود'

    def __str__(self):
        last_change_timestamp = timestamp_formatter(self.timestamp)
        created_timestamp = timestamp_formatter(self.created)
        return f'حواله ورود شماره {self.id} - ساخته شده در: {created_timestamp} - آخرین تغییر: {last_change_timestamp}'

    def delete(self, using=None, keep_parents=False):
        for detail in self.inputdetail_set.all():
            product_record = detail.get_product_record()
            product_record.inventory -= detail.value
            product_record.save()
            if product_record.inventory == 0:
                product_record.delete()
        super(Input, self).delete(using, keep_parents)


class InputDetail(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, verbose_name='محصول')
    input = models.ForeignKey(Input, models.CASCADE, verbose_name='حواله ورود')
    value = models.PositiveIntegerField(verbose_name='مقدار ورودی')

    __old_value = None
    __old_product_id = None

    class Meta:
        verbose_name = 'جزییات حواله ورود'
        verbose_name_plural = 'جزییات های حواله ورود'

    def __str__(self):
        return f'مقدار ورودی: {self.value} - محصول: {self.product.title}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_value = self.value
        self.__old_product_id = self.product_id

    def get_product_record(self):
        try:
            return self.input.store.productrecord_set.filter(product_id=self.product.id).first()
        except Exception:
            return None

    def get_old_product_record(self):
        try:
            return self.input.store.productrecord_set.filter(product_id=self.__old_product_id).first()
        except Exception:
            return None

    def get_final_value(self):
        value = self.value
        if self.__old_value:
            value = self.value - self.__old_value
        return value

    def clean(self):
        try:
            self.product
        except ObjectDoesNotExist:
            raise ValidationError('یک محصول انتخاب کنید.')
        if not self.value:
            raise ValidationError('مقدار ورودی را وارد کنید.')
        if self.__old_product_id is not None and self.__old_product_id != self.product_id:
            product_record = self.get_old_product_record()
            if product_record:
                if product_record.inventory < self.__old_value:
                    raise ValidationError(
                        f'موجودی محصول {product_record.product.title} {product_record.inventory} {self.product.measuring_unit.title} است.'
                        ' حواله های خروج را بررسی کنید.')
        else:
            product_record = self.get_product_record()
            value = self.get_final_value()
            if product_record:
                if product_record.inventory + value < 0:
                    raise ValidationError(
                        f'موجودی محصول {self.product.title} {product_record.inventory} {self.product.measuring_unit.title} است.'
                        ' حواله های خروج را بررسی کنید.')

    def delete(self, using=None, keep_parents=False):
        product_record = self.get_old_product_record()
        product_record.inventory -= self.__old_value
        product_record.save()
        if product_record.inventory == 0:
            product_record.delete()
        super(InputDetail, self).delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        value = self.get_final_value()
        if self.__old_product_id is not None and self.__old_product_id != self.product_id:
            value = self.value
            product_record = self.get_old_product_record()
            if product_record:
                product_record.inventory -= self.__old_value
                product_record.save()
                if product_record.inventory == 0:
                    product_record.delete()
        product_record = self.get_product_record()
        if product_record is None:
            product_record = ProductRecord.objects.create(store=self.input.store, product=self.product)
            value = self.value
        product_record.inventory += value
        product_record.save()
        if product_record.inventory == 0:
            product_record.delete()
        # Updating the old variables
        self.__old_product_id = self.product_id
        self.__old_value = self.value
        # Updating the related <store> timestamp
        self.input.store.save()
        super(InputDetail, self).save(force_insert, force_update)


class OutputManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(cause__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Output(models.Model):
    store = models.ForeignKey(Store, models.CASCADE, verbose_name='انبار')
    cause = models.CharField(max_length=300, verbose_name='بابت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='تاریخ و زمان')

    objects = OutputManager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'حواله خروج'
        verbose_name_plural = 'حواله های خروج'

    def __str__(self):
        last_change_timestamp = timestamp_formatter(self.timestamp)
        created_timestamp = timestamp_formatter(self.created)
        return f'حواله خروج شماره {self.id} - ساخته شده در: {created_timestamp} - آخرین تغییر: {last_change_timestamp}'

    def delete(self, using=None, keep_parents=False):
        for detail in self.outputdetail_set.all():
            product_record = detail.get_product_record()
            product_record.inventory += detail.value
            product_record.save()
            if product_record.inventory == 0:
                product_record.delete()
        super(Output, self).delete(using, keep_parents)


class OutputDetail(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, verbose_name='محصول')
    output = models.ForeignKey(Output, models.CASCADE, verbose_name='حواله خروج')
    value = models.PositiveIntegerField(verbose_name='مقدار خروجی')

    __old_value = None
    __old_product_id = None

    class Meta:
        verbose_name = 'جزییات حواله خروج'
        verbose_name_plural = 'جزییات های حواله خروج'

    def __str__(self):
        return f'مقدار خروجی: {self.value} - محصول: {self.product.title}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_value = self.value
        self.__old_product_id = self.product_id

    def get_product_record(self):
        try:
            return self.output.store.productrecord_set.filter(product_id=self.product.id).first()
        except Exception:
            return None

    def get_old_product_record(self):
        try:
            return self.output.store.productrecord_set.filter(product_id=self.__old_product_id).first()
        except Exception:
            return None

    def get_final_value(self):
        value = self.value
        if self.__old_value:
            value = self.value - self.__old_value
        return value

    def clean(self):
        try:
            self.product
        except ObjectDoesNotExist:
            raise ValidationError('یک محصول انتخاب کنید.')
        if not self.value:
            raise ValidationError('مقدار خروجی را وارد کنید.')
        value = self.get_final_value()
        product_record = self.output.store.productrecord_set.filter(product=self.product).first()
        if self.__old_product_id is not None and self.__old_product_id != self.product_id:
            value = self.__old_value
            product_record = self.get_old_product_record()
        if product_record:
            if product_record.inventory - value < 0:
                raise ValidationError(
                    f'موجودی محصول {self.product.title} {product_record.inventory} {self.product.measuring_unit.title} است.'
                    ' حواله های ورود را بررسی کنید.')
        else:
            raise ValidationError(
                f'موجودی محصول {self.product.title} ۰ {self.product.measuring_unit.title} است.'
                ' حواله های ورود را بررسی کنید.')

    def delete(self, using=None, keep_parents=False):
        product_record = self.get_old_product_record()
        product_record.inventory += self.__old_value
        product_record.save()
        if product_record.inventory == 0:
            product_record.delete()
        super(OutputDetail, self).delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        value = self.get_final_value()
        if self.__old_product_id is not None and self.__old_product_id != self.product_id:
            value = self.value
            product_record = self.get_old_product_record()
            if product_record:
                product_record.inventory += self.__old_value
                product_record.save()
                if product_record.inventory == 0:
                    product_record.delete()
        product_record = self.get_product_record()
        product_record.inventory -= value
        product_record.save()
        if product_record.inventory == 0:
            product_record.delete()
        # Updating the old variables
        self.__old_product_id = self.product_id
        self.__old_value = self.value
        # Updating the related <store> timestamp
        self.output.store.save()
        super(OutputDetail, self).save(force_insert, force_update)
