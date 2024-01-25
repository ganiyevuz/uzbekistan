from django.contrib import admin
from django.contrib.admin import ModelAdmin

from uzbekistan.models import Region, District


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ('name_uz', 'name_oz', 'name_ru', 'name_en')
    search_fields = ('name_uz', 'name_oz', 'name_ru', 'name_en')
    sortable_by = ('name_uz', 'name_oz', 'name_ru', 'name_en')


@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = ('name_uz', 'name_oz', 'name_ru', 'get_region_name')
    search_fields = ('name_uz', 'name_oz', 'name_ru', 'get_region_name')
    sortable_by = ('name_uz', 'name_oz', 'name_ru', 'region')
    save_on_top = True

    def get_region_name(self, obj):
        return obj.region.name_uz

    get_region_name.short_description = 'Region'
