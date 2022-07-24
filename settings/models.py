from django.core.validators import FileExtensionValidator
from django.db import models

from config.DateTimeRelated.DateTimeFormatter import timestamp_formatter
from config.Models.SingleTon import SingletonModel


class SiteSettings(SingletonModel):
    # Major part --------------------------------------------------------------------------------------------
    title = models.CharField(max_length=150, verbose_name="عنوان سایت")
    site_url = models.URLField(verbose_name="آدرس دامنه سایت")
    short_des = models.CharField(max_length=300, null=True, blank=True, verbose_name="توضیحات کوتاه")
    email = models.EmailField(max_length=100, verbose_name="پست الکترونیک")
    about_us = models.TextField(null=True, blank=True, verbose_name="درباره ما")
    copy_right = models.TextField(null=True, blank=True, verbose_name="متن کپی رایت")
    logo_image = models.FileField(upload_to='settings/', null=True, blank=True, verbose_name="تصویر لوگو",
                                  validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])])
    fav_icon = models.FileField(upload_to='settings/', null=True, blank=True, verbose_name="فاوآیکون",
                                validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])])
    # Timestamp ---------------------------------------------------------------------------------------------
    timestamp = models.DateTimeField(auto_now=True, verbose_name="تاریخ و زمان")

    class Meta:
        verbose_name = 'تنظیمات'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        timestamp = timestamp_formatter(self.timestamp)
        return f'{self.title if self.title else self.id} - آخرین تغییر: {timestamp}'


class BackgroundImage(models.Model):
    settings = models.ForeignKey(SiteSettings, models.CASCADE, verbose_name="تنظیمات")
    image = models.ImageField(upload_to='settings/', verbose_name="عکس")

    class Meta:
        verbose_name = 'عکس پس زمینه'
        verbose_name_plural = 'عکس های پس زمینه'

    def __str__(self):
        return 'عکس پس زمینه'
