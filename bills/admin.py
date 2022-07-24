from django.contrib import admin

from .models import (
    InputDetail,
    Input,
    OutputDetail,
    Output,
)
from .utils import check_input_delete_permission


class InputDetailInline(admin.TabularInline):
    model = InputDetail
    extra = 0
    autocomplete_fields = ['product']

    def has_delete_permission(self, request, obj=None):
        return check_input_delete_permission(obj)


class InputAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'store_id']
    inlines = [InputDetailInline]
    ordering = ['-created']
    actions = None

    def get_readonly_fields(self, request, obj=None):
        fields = super(InputAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return fields + ('store',)
        else:
            return fields

    def has_delete_permission(self, request, obj=None):
        return check_input_delete_permission(obj)


class OutputDetailInline(admin.TabularInline):
    model = OutputDetail
    extra = 0
    autocomplete_fields = ['product']


class OutputAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'cause', 'store_id']
    inlines = [OutputDetailInline]
    ordering = ['-created']
    actions = None

    def get_readonly_fields(self, request, obj=None):
        fields = super(OutputAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return fields + ('store',)
        else:
            return fields


admin.site.register(Input, InputAdmin)
admin.site.register(Output, OutputAdmin)
