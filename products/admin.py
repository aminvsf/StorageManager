from django.contrib import admin

from .models import (
    MeasuringUnit,
    Product,
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'measuring_unit']
    search_fields = ['title']


admin.site.register(MeasuringUnit)
admin.site.register(Product, ProductAdmin)
