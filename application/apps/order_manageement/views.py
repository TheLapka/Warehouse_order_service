from rest_framework.views import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.order_manageement.entities import ProductInOrderEntity, UserEntity
from apps.order_manageement.serializers import AddProductInViewSerializer
from rest_framework import status

from apps.order_manageement.services import AddProductInOrderService


class AddProductInOrderView(GenericAPIView):
    serializer_class = AddProductInViewSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        sz = AddProductInViewSerializer(data=request.data, many=True)
        sz.is_valid(raise_exception=True)

        creator = AddProductInOrderService()
        creator.add_product_in_order(
            [
                ProductInOrderEntity(product_id=el["product_id"], amount=el["amount"])
                for el in sz.data
            ], UserEntity(user_id=request.user.pk, email=request.user.email)
        )
        return Response(status=status.HTTP_201_CREATED)
