from decimal import Decimal
from typing import Optional, TypedDict

from apps.warehouse_management.models import Product, Stock
from django.db import IntegrityError
from django.db.models import F


class ProductCreate(TypedDict):
    name: str
    supplier_id: int
    cat_id: int
    price: Decimal


class DuplicateSupplierNameException(Exception):
    pass


class ProductRepository:
    def get_product(self, pk: int) -> Optional[Product]:
        product = Product.objects.filter(pk=pk).first()
        return product

    def create_product(self, data: ProductCreate) -> Optional[Product]:
        try:
            return Product.objects.create(
                name=data["name"],
                supplier_id=data["supplier_id"],
                cat_id=data["cat_id"],
                price=data["price"],
            )
        except IntegrityError as e:
            raise DuplicateSupplierNameException


class AddProductInWarehouse(TypedDict):
    product_id: int
    amount: int


class DataBaseUnavailable(Exception):
    pass


class ProductInWarehouseRepository:
    def get_product_in_stock(self, pk: int) -> Optional[Stock]:
        product_in_stock = Stock.objects.filter(product=pk).first()
        return product_in_stock

    def get_product(self, pk: int) -> Optional[Product]:
        return Product.objects.filter(pk=pk).first()

    def add_product_in_stock(self, product_id: int, amount: int) -> Stock:
        return Stock.objects.create(product_id=product_id, amount=amount)

    def update_amount(self, product_id: int, amo: int) -> Stock:
        Stock.objects.filter(product_id=product_id).update(amount=F("amount") + amo)
        res = Stock.objects.filter(product=product_id).first()
        return res
