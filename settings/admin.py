from django.db import models
from django.contrib import admin
from django.db.utils import ProgrammingError
from django.forms import TextInput

from settings.models import SiteSettings, BackgroundImage


class BackgroundImageInline(admin.StackedInline):
    model = BackgroundImage
    extra = 0


class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = (BackgroundImageInline,)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
        models.IntegerField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vIntegerField'})},
        models.URLField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vURLField'})},
    }

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            SiteSettings.load().save()
        except ProgrammingError:
            pass

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(SiteSettings, SiteSettingsAdmin)
