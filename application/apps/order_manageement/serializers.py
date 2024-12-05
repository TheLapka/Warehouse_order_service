from rest_framework import serializers


class AddProductInViewSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    amount = serializers.IntegerField()
