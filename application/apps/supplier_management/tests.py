from apps.supplier_management.models import Supplier
from apps.supplier_management.serializer import SupplierSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SupplierAPITestCase(APITestCase):
    def test_get(self) -> None:
        supplier_1 = Supplier.objects.create(
            country="TestStrana", city="TestCity", building="1", name="OOO TEST"
        )
        supplier_2 = Supplier.objects.create(
            country="TestStrana2", city="TestCity2", building="2", name="OOO TEST2"
        )
        url = reverse("supplier-list")
        response = self.client.get(url)
        serializer_data = SupplierSerializer([supplier_1, supplier_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class SupplierSerializerTestCase(TestCase):
    def test_serik(self) -> None:
        supplier_1 = Supplier.objects.create(
            country="TestStrana", city="TestCity", building="1", name="OOO TEST"
        )
        supplier_2 = Supplier.objects.create(
            country="TestStrana2", city="TestCity2", building="2", name="OOO TEST2"
        )
        data_serik = SupplierSerializer([supplier_1, supplier_2], many=True).data
        expected_data = [
            {
                "id": supplier_1.pk,
                "country": "TestStrana",
                "city": "TestCity",
                "building": 1,
                "name": "OOO TEST",
            },
            {
                "id": supplier_2.pk,
                "country": "TestStrana2",
                "city": "TestCity2",
                "building": 2,
                "name": "OOO TEST2",
            },
        ]
        self.assertEqual(expected_data, data_serik)
