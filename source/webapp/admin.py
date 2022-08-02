from django.contrib import admin

# Register your models here.
from webapp.models import Product, CartProduct, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'remainder', 'price']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'category', 'remainder', 'price']


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity']
    list_display_links = ['product']
    list_filter = ['product']
    search_fields = ['product']
    fields = ['quantity']


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'quantities', 'username', 'address', 'created_at']
#     list_display_links = ['products']
#     list_filter = ['products', 'username']
#     search_fields = ['products']
#     fields = ['quantities', 'username', 'address']
#     readonly_fields = ['created_at']


admin.site.register(Product, ProductAdmin)
admin.site.register(CartProduct, CartProductAdmin)
# admin.site.register(Order, OrderAdmin)
