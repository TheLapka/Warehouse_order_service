# Generated by Django 5.1.3 on 2024-12-06 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order_manageement', '0001_initial'),
        ('warehouse_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Заказчик'),
        ),
        migrations.AddField(
            model_name='productonorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_manageement.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='productonorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse_management.product', verbose_name='Товар'),
        ),
    ]