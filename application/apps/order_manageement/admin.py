from apps.order_manageement.models import Order, ProductOnOrder
from apps.warehouse_management.models import Category, Product, Stock
from django.contrib import admin


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "order_date")


class ProductOnOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "amount", "purchase_price")



admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOnOrder, ProductOnOrderAdmin)

