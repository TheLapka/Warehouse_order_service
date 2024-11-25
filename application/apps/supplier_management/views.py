from apps.supplier_management.models import Supplier
from apps.supplier_management.serializer import SupplierSerializer
from rest_framework.viewsets import ModelViewSet


class SupplierView(ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
