from apps.warehouse_management.models import Category, Product, Stock
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "cat")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "cat", "price", "supplier")


class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "amount")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
