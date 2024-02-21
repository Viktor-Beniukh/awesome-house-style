from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from goods.models import Category, Product
from orders.models import Order, OrderItem


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )

        Order.objects.create(user=user)

    def test_order_str(self):
        order = Order.objects.get(id=1)

        self.assertEqual(
            str(order),
            f"Order № {order.pk} | Consumer {order.user.first_name} {order.user.last_name}"
        )

    def test_update_order_status(self):
        order = Order.objects.get(id=1)

        order.status_order = Order.INPROCESSING
        order.save()

        self.assertEqual(order.status_order, Order.INPROCESSING)

    def test_calculate_total_price_and_quantity(self):
        order = Order.objects.get(id=1)

        category = Category.objects.create(name="Test", slug="test")

        product1 = Product.objects.create(
            name="Test Product 1",
            description="Test Description Product 1",
            price=50.00,
            discount=0.0,
            quantity=2,
            category=category
        )

        product2 = Product.objects.create(
            name="Test Product 2",
            description="Test Description Product 2",
            price=40.00,
            discount=0.0,
            quantity=1,
            category=category
        )

        order_item1 = OrderItem.objects.create(
            order=order, product=product1, price=product1.price, quantity=product1.quantity
        )
        order_item2 = OrderItem.objects.create(
            order=order, product=product2, price=product2.price, quantity=product2.quantity
        )

        order.order_items.set([order_item1, order_item2])

        expected_total_price = Decimal("140.00")
        expected_total_quantity = 3

        total_price = order.order_items.total_price()
        total_quantity = order.order_items.total_quantity()

        self.assertEqual(total_price, expected_total_price)
        self.assertEqual(total_quantity, expected_total_quantity)


class OrderItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )
        category = Category.objects.create(
            name="Test",
            slug="test"
        )
        product = Product.objects.create(
            name="Test Product",
            description="Test Description Product",
            price=50.00,
            discount=10.0,
            quantity=2,
            category=category
        )
        order = Order.objects.create(user=user)

        OrderItem.objects.create(
            order=order, product=product, price=product.price, quantity=product.quantity
        )

    def test_order_item_str(self):
        order_item = OrderItem.objects.get(id=1)

        self.assertEqual(
            str(order_item),
            f'Product "{order_item.name}" | Order № {order_item.order.pk}'
        )

    def test_calculate_product_price(self):
        order_item = OrderItem.objects.get(id=1)
        product_price = order_item.products_price()
        expected_product_price = Decimal("90.00")

        self.assertEqual(product_price, expected_product_price)

    def test_calculate_quantity(self):
        order_item = OrderItem.objects.get(id=1)
        quantity = order_item.quantity
        expected_quantity = 2

        self.assertEqual(quantity, expected_quantity)

    def test_validate_quantity(self):
        order_item = OrderItem.objects.get(id=1)
        order_item.quantity = -1

        with self.assertRaises(ValidationError):
            order_item.full_clean()
