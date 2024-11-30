from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    supplier = serializers.CharField()
    cat = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)


class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    supplier_id = serializers.IntegerField()
    cat_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)


class AddProductInStokSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class ProductInStockSerializer(serializers.Serializer):
    product = serializers.CharField()
    amount = serializers.IntegerField()
