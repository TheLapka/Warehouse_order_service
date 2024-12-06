from apps.warehouse_management.models import Stock
from django.db.models import QuerySet


class ProductInOrderRep:
    def get_product_in_stok(self, list_pk: list[int]) -> list[Stock]:
        return list(Stock.objects.filter(product__pk__in=list_pk))