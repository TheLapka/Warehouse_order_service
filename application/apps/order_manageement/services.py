from apps.order_manageement.entities import ProductInOrderEntity, UserEntity
from apps.order_manageement.models import Order, ProductOnOrder
from apps.order_manageement.repositories import ProductInOrderRep
from apps.user_and_email_manager.email_gateway import EmailGateway
from apps.warehouse_management.models import Stock
from django.db.models import F
from rest_framework.serializers import ValidationError


class AddProductInOrderService:
    def add_product_in_order(self, data: list[ProductInOrderEntity], user: UserEntity):
        rep = ProductInOrderRep()
        product_ids = [el.product_id for el in data]
        data_ids_and_prod_entity_mapping = {el.product_id: el for el in data}
        stocks = rep.get_product_in_stok(product_ids)
        product_in_stock_ids = [el.product.pk for el in stocks]
        ids_and_stock_mapping = {el.product.pk: el for el in stocks}
        self._checking_existence_of_goods(product_ids, product_in_stock_ids)
        prod_ids_and_amount_mapping = {el.product_id: el.amount for el in data}
        self._checking_the_availability_of_goods(stocks, prod_ids_and_amount_mapping)
        # with Транзакция
        self._create_order_and_products_order(user.user_id, data, ids_and_stock_mapping)
        self._update_amount_products_in_warehouse(
            data_ids_and_prod_entity_mapping, stocks
        )

        self._send_email_after_creating_order(data, user.email)

    def _checking_existence_of_goods(
        self, product_ids: list[int], product_in_stock_ids: list[int]
    ) -> None:
        if set(product_ids) != set(product_in_stock_ids):
            err_products_ids = set(product_ids) - set(product_in_stock_ids)
            raise ValidationError(
                detail=f"Товары с id {err_products_ids} не существует"
            )

    def _checking_the_availability_of_goods(self, stocks: list[Stock], dic: dict):
        non_product = []
        for stock in stocks:
            if stock.amount >= dic[stock.product.pk]:
                non_product.append(stock.product.pk)
        if not non_product:
            raise ValidationError(
                detail=f"Проверьте наличие данных товаров {non_product}"
            )

    def _create_order_and_products_order(
        self, user_id: int, data: list[ProductInOrderEntity], stocks: dict[int, Stock]
    ):

        order = Order.objects.create(user_id=user_id)
        products_on_order = [
            ProductOnOrder(
                order_id=order.pk,
                product_id=el.product_id,
                amount=el.amount,
                purchase_price=stocks[el.product_id].product.price,
            )
            for el in data
        ]
        ProductOnOrder.objects.bulk_create(products_on_order)

    def _update_amount_products_in_warehouse(
        self, data: dict[int:ProductInOrderEntity], stocks: list[Stock]
    ):
        for stock in stocks:
            stock.amount = F("amount") - data[stock.product.pk].amount
        Stock.objects.bulk_update(stocks, ["amount"])

    def _send_email_after_creating_order(
        self, data: list[ProductInOrderEntity], email: str
    ):
        EmailGateway().send_email(purpose="pay_prod", email=email, data=data)
