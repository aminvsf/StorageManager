from django.contrib import admin

from .models import Store, ProductRecord
from bills.models import Input, Output


class InputInline(admin.TabularInline):
    model = Input
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OutputInline(admin.TabularInline):
    model = Output
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ProductRecordInline(admin.TabularInline):
    model = ProductRecord
    extra = 0
    autocomplete_fields = ['product']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class StoreAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'timestamp', 'name', 'user']
    inlines = [InputInline, OutputInline, ProductRecordInline]
    ordering = ['-created']


class ProductRecordAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'store', 'inventory']
    list_filter = ['store']
    list_editable = ['inventory']
    search_fields = ['store__id', 'product__title', 'store__user__first_name']

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(Store, StoreAdmin)
admin.site.register(ProductRecord, ProductRecordAdmin)
