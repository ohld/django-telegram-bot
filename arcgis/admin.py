from django.contrib import admin

# Register your models here.
from arcgis.models import Arcgis


@admin.register(Arcgis)
class UserAdmin(admin.ModelAdmin):
    list_display = ('location', 'city', 'country_code')
    list_filter = ('country_code',)
