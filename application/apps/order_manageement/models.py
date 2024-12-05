from django.db import models
from apps.user_and_email_manager.models import CustomUser
from apps.warehouse_management.models import Product

class Order(models.Model):
    order_date = models.DateField(auto_now_add=True, verbose_name="Дата заказа")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Заказчик"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"{self.user}"


class ProductOnOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    amount = models.PositiveIntegerField(verbose_name="Кол-во")
    purchase_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Закупочная цена"
    )

    class Meta:
        verbose_name = "Продукт в заказе"
        verbose_name_plural = "Продукты в заказе"

    def __str__(self):
        return self.name
