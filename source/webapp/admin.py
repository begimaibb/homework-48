from django.contrib import admin

# Register your models here.
from webapp.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'remainder', 'price']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'category', 'remainder', 'price']


admin.site.register(Product, ProductAdmin)

