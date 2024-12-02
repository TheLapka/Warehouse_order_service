# Generated by Django 5.1.3 on 2024-12-02 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('supplier_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название категории')),
                ('cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse_management.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse_management.category', verbose_name='Категория')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier_management.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='Кол-во товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse_management.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар на складе',
                'verbose_name_plural': 'Товары на складе',
            },
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('name', 'supplier'), name='unique_product_constraint'),
        ),
    ]
