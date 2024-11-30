from apps.warehouse_management.models import Product, Stock
from apps.warehouse_management.repositories import (
    DuplicateSupplierNameException,
    ProductInWarehouseRepository,
    ProductRepository,
)
from apps.warehouse_management.serializer import (
    AddProductInStokSerializer,
    CreateProductSerializer,
    ProductInStockSerializer,
    ProductSerializer,
)
from apps.warehouse_management.services import StockServices
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import Response


class RetrieveUpdateDeleteProductView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk: int):
        get = ProductRepository()
        result = get.get_product(pk)
        sz = ProductSerializer(instance=result)
        return Response(data=sz.data, status=status.HTTP_200_OK)


class CreateProductView(CreateAPIView):
    serializer_class = CreateProductSerializer

    def post(self, request):
        sz = CreateProductSerializer(data=request.data)
        sz.is_valid(raise_exception=True)

        repo = ProductRepository()
        try:
            result = repo.create_product(sz.data)
        except DuplicateSupplierNameException:
            return Response(
                data={"error": "Такой товар от этого поставщика уже существует"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        sz = ProductSerializer(instance=result)
        return Response(data=sz.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return super().get_serializer_class()


class GetAllProductsView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Product]:
        qs = Product.objects.all()
        supplier = self.request.query_params.get("supplier")
        product_name = self.request.query_params.get("product_name")
        if supplier is not None:
            qs = qs.filter(supplier__name__icontains=supplier)
        if product_name is not None:
            qs = qs.filter(name__icontains=product_name)
        return qs


class AddProductInWarehouseView(CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = AddProductInStokSerializer

    def post(self, request):
        sz = AddProductInStokSerializer(data=request.data)
        sz.is_valid(raise_exception=True)

        srv = StockServices(ProductInWarehouseRepository())
        result = srv.add_or_update_product_to_stock(
            product_id=sz.data["product_id"], amount=sz.data["amount"]
        )

        sz = ProductInStockSerializer(instance=result)
        return Response(data=sz.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return super().get_serializer_class()


class GetAllProductsInWarehouseView(ListAPIView):
    serializer_class = ProductInStockSerializer
    queryset = Stock.objects.all()
    pagination_class = LimitOffsetPagination


class GetProductInWarehouseView(RetrieveAPIView):
    serializer_class = ProductInStockSerializer
    queryset = Stock.objects.all()

    def get(self, request, pk: int) -> Response:
        repo = ProductInWarehouseRepository()
        result = repo.get_product_in_stock(pk)
        sz = ProductInStockSerializer(instance=result)
        return Response(data=sz.data, status=status.HTTP_200_OK)
