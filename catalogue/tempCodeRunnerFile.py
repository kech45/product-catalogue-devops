from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from .models import Product


class ProductModelTest(TestCase):

    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal("99.99"),
            stock_quantity=10,
            is_active=True,
        )

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, Decimal("99.99"))
        self.assertIsInstance(product.price, Decimal)

    def test_product_price_decimal(self):
        product = Product.objects.create(name="Decimal Product", price=Decimal("49.50"))

        self.assertIsInstance(product.price, Decimal)


class ProductAPITest(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="API Product",
            description="API Desc",
            price=Decimal("25.00"),
            stock_quantity=5,
        )
        self.list_url = reverse("product-list-create")
        self.detail_url = reverse("product-detail", args=[self.product.id])

    def test_get_product_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "API Product")

    def test_get_nonexistent_product(self):
        url = reverse("product-detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        data = {
            "name": "New Product",
            "description": "New Desc",
            "price": "99.99",
            "stock_quantity": 3,
            "is_active": True,
        }

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_invalid_price(self):
        data = {"name": "Bad Product", "price": "abc"}

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        data = {
            "name": "Updated Product",
            "description": "Updated Desc",
            "price": "30.00",
            "stock_quantity": 8,
            "is_active": False,
        }

        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    def test_partial_update_product(self):
        data = {"name": "Partially Updated"}

        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
