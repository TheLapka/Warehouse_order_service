from apps.warehouse_management.models import Stock
from apps.warehouse_management.repositories import ProductInWarehouseRepository


class StockServices:
    def __init__(self, stock_repo: ProductInWarehouseRepository) -> None:
        self._stock_repo = stock_repo

    def add_or_update_product_to_stock(self, product_id: int, amount: int) -> Stock:
        stock = self._stock_repo.get_product_in_stock(pk=product_id)

        if stock is None:
            stock = self._stock_repo.add_product_in_stock(
                product_id=product_id, amount=amount
            )
            return stock
        else:
            stock = self._stock_repo.update_amount(product_id, amount)
            return stock
