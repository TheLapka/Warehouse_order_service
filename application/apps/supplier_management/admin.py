from apps.supplier_management.models import Supplier
from django.contrib import admin


class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "building")


admin.site.register(Supplier, SupplierAdmin)
