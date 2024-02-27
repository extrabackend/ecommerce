from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'is_active', 'is_top')
    list_display_links = ('id', 'title')
    list_editable = ('is_active', 'is_top')
    list_filter = ('is_active', 'is_top', 'created_at')
    search_fields = ('title',)


admin.site.register(models.Category)
admin.site.register(models.Subcategory)
