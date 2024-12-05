from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.order_manageement.serializers import AddProductInViewSerializer
from rest_framework import status

class AddProductInOrderView(GenericAPIView):
    serializer_class = AddProductInViewSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        sz = AddProductInViewSerializer(data=request.data, many=True)
        sz.is_valid(raise_exception=True)

        creator = EmailConfirmationService()
        creator.create_order(request.user.email, sz.data["code"])
        return Response(status=status.HTTP_201_CREATED)
