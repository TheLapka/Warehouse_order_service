from apps.supplier_management.models import Supplier
from django.db import models


class Category(models.Model):
    name = models.CharField("Название категории", max_length=50)
    cat = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Подкатегория",
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField("Название товара", max_length=50)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, verbose_name="Поставщик"
    )
    cat = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    amount = models.PositiveIntegerField("Кол-во товара")

    def __str__(self) -> str:
        return f"{self.product}"

    class Meta:
        verbose_name = "Товар на складе"
        verbose_name_plural = "Товары на складе"
