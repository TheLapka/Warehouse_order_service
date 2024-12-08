from apps.supplier_management.models import Supplier
from apps.warehouse_management.models import Category, Product
from apps.warehouse_management.serializer import ProductSerializer
from rest_framework import status
from rest_framework.test import APITestCase


class ProductAPITestCase(APITestCase):
    def test_get_all_products(self) -> None:
        cat = Category.objects.create(name="Test")
        supl_1 = Supplier.objects.create(
            country="TestStrana", city="TestCity", building="1", name="OOO TEST"
        )
        supl_2 = Supplier.objects.create(
            country="TestStrana2", city="TestCity2", building="2", name="OOO TEST2"
        )
        prod_1 = Product.objects.create(
            name="TEST1", supplier_id=1, cat_id=1, price=543.21
        )
        prod_2 = Product.objects.create(
            name="TEST2", supplier_id=2, cat_id=1, price=543.55
        )

        url = "http://127.0.0.1:8000/products/"
        print(url)
        response = self.client.get(url)
        seri = ProductSerializer([prod_1, prod_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(seri, response.data["results"])

    def test_get_product(self) -> None:
        cat = Category.objects.create(name="Test")
        supl_1 = Supplier.objects.create(
            country="TestStrana", city="TestCity", building="1", name="OOO TEST"
        )
        prod_1 = Product.objects.create(
            name="TEST1", supplier_id=1, cat_id=1, price=543.21
        )
        prod_2 = Product.objects.create(
            name="TEST2", supplier_id=1, cat_id=1, price=543.20
        )
        url = "http://127.0.0.1:8000/products/1"
        response = self.client.get(url)
        seri = ProductSerializer(prod_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(seri.data, response.data)


# class SupplierAPITestCase(APITestCase):
#     def test_get(self) -> None:
#         supplier_1 = Supplier.objects.create(
#             country="TestStrana", city="TestCity", building="1", name="OOO TEST"
#         )
#         supplier_2 = Supplier.objects.create(
#             country="TestStrana2", city="TestCity2", building="2", name="OOO TEST2"
#         )
#         url = reverse("supplier-list")
#         response = self.client.get(url)
#         serializer_data = SupplierSerializer([supplier_1, supplier_2], many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)


# class SupplierSerializerTestCase(TestCase):
#     def test_serik(self) -> None:
#         supplier_1 = Supplier.objects.create(
#             country="TestStrana", city="TestCity", building="1", name="OOO TEST"
#         )
#         supplier_2 = Supplier.objects.create(
#             country="TestStrana2", city="TestCity2", building="2", name="OOO TEST2"
#         )
#         data_serik = SupplierSerializer([supplier_1, supplier_2], many=True).data
#         expected_data = [
#             {
#                 "id": supplier_1.pk,
#                 "country": "TestStrana",
#                 "city": "TestCity",
#                 "building": 1,
#                 "name": "OOO TEST",
#             },
#             {
#                 "id": supplier_2.pk,
#                 "country": "TestStrana2",
#                 "city": "TestCity2",
#                 "building": 2,
#                 "name": "OOO TEST2",
#             },
#         ]
#         self.assertEqual(expected_data, data_serik)
