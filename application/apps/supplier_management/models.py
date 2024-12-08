from django.db import models


class Supplier(models.Model):
    country = models.CharField("Страна", max_length=50)
    city = models.CharField("Город", max_length=50)
    building = models.PositiveIntegerField("Номер здания")
    name = models.CharField("Наименование организации", max_length=100, unique=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self) -> str:
        return f"{self.name}"
