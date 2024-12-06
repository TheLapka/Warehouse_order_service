from rest_framework import serializers


class AddProductInViewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()
