from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch

from goods.models import Category, Product
from orders.models import Order, OrderItem
from carts.models import Cart


User = get_user_model()


class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="testpass",
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Test Category", slug="test-category")

        self.product1 = Product.objects.create(
            name="Test Product 1",
            description="Test Description Product 1",
            price=50.00,
            discount=2.0,
            quantity=5,
            category=self.category
        )

        self.product2 = Product.objects.create(
            name="Test Product 2",
            description="Test Description Product 2",
            price=40.00,
            discount=0.0,
            quantity=3,
            category=self.category
        )

    def test_create_order_view_get(self):
        response = self.client.get(reverse("orders:create_order"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/create_order.html")

    def test_create_order_view_post_success(self):
        order = Order.objects.create(user=self.user)
        cart1 = Cart.objects.create(user=self.user, product=self.product1, quantity=3)
        cart2 = Cart.objects.create(user=self.user, product=self.product2, quantity=2)

        cart_item1 = OrderItem.objects.create(
            order=order, product=cart1.product, price=cart1.product.sell_price(), quantity=cart1.quantity
        )
        cart_item2 = OrderItem.objects.create(
            order=order, product=cart2.product, price=cart2.product.sell_price(), quantity=cart2.quantity
        )

        order.order_items.set([cart_item1, cart_item2])

        response = self.client.post(reverse("orders:create_order"), {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "phone_number": "+1234567890231",
            "requires_delivery": "1",
            "shipping_address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
            "zipcode": 12345,
            "payment_on_get": "1"
        })

        cart_items = Cart.objects.filter(user=self.user)
        cart_items.delete()

        self.product1.quantity -= cart_item1.quantity
        self.product2.quantity -= cart_item2.quantity
        self.product1.save()
        self.product2.save()

        self.assertEqual(self.product1.quantity, 2)
        self.assertEqual(self.product2.quantity, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)
        self.assertEqual(Cart.objects.count(), 0)

    def test_insufficient_quantity_in_cart(self):
        Cart.objects.create(user=self.user, product=self.product1, quantity=6)
        Cart.objects.create(user=self.user, product=self.product2, quantity=3)

        self.assertEqual(self.product1.quantity, 5)
        self.assertEqual(self.product2.quantity, 3)

        self.assertEqual(Cart.objects.count(), 2)

        for cart_item in Cart.objects.all():
            if cart_item.quantity > cart_item.product.quantity:
                self.assertTrue(f"Insufficient quantity for product {cart_item.product.name}")

        self.assertEqual(Order.objects.count(), 0)

        self.assertEqual(Cart.objects.count(), 2)

    @patch("stripe.checkout.Session.create")
    def test_create_checkout_session(self, mock_stripe_session_create):
        order = Order.objects.create(user=self.user)
        mock_stripe_session_create.return_value.id = "test_session_id"
        mock_stripe_session_create.return_value.url = "https://example.com/checkout"

        response = self.client.get(reverse("orders:create-checkout-session", args=[order.id]))

        self.assertEqual(response.status_code, 302)

        order.refresh_from_db()
        session_id = mock_stripe_session_create.return_value.id

        self.assertEqual(order.session_id, session_id)

    def test_success_view(self):
        order = Order.objects.create(
            user=self.user, session_id="test_session_id", status_payment=Order.PENDING
        )

        response = self.client.get(reverse("orders:success"))

        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()

        self.assertEqual(order.status_payment, Order.PAID)
        self.assertEqual(order.is_paid, True)
        self.assertEqual(order.status_order, Order.SHIPPED)

    def test_cancel_view(self):
        order = Order.objects.create(
            user=self.user, session_id="test_session_id", status_payment=Order.PENDING
        )

        response = self.client.get(reverse("orders:cancel"))

        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()

        self.assertEqual(order.status_payment, Order.CANCELLED)
