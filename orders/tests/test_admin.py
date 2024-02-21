from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from orders.admin import OrderAdmin, OrderItemAdmin
from orders.models import Order, OrderItem


class OrderAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.order_admin = OrderAdmin(Order, self.admin_site)

    def test_order_admin_list_display(self):
        expected_list_display = (
            "id",
            "user",
            "requires_delivery",
            "status_order",
            "status_payment",
            "payment_on_get",
            "is_paid",
            "created_at",
        )
        self.assertEqual(self.order_admin.list_display, expected_list_display)

    def test_order_admin_list_editable(self):
        expected_list_editable = (
            "status_order",
            "is_paid",
            "payment_on_get"
        )
        self.assertEqual(self.order_admin.list_editable, expected_list_editable)

    def test_order_admin_search_fields(self):
        expected_search_fields = ("id",)
        self.assertEqual(self.order_admin.search_fields, expected_search_fields)

    def test_order_admin_list_filter(self):
        expected_list_filter = (
            "requires_delivery",
            "status_order",
            "payment_on_get",
            "is_paid",
        )
        self.assertEqual(self.order_admin.list_filter, expected_list_filter)


class OrderItemAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.order_item_admin = OrderItemAdmin(OrderItem, self.admin_site)

    def test_order_item_admin_list_display(self):
        expected_list_display = ("order", "product", "name", "price", "quantity")
        self.assertEqual(self.order_item_admin.list_display, expected_list_display)

    def test_order_item_admin_search_fields(self):
        expected_search_fields = ("order", "product", "name",)
        self.assertEqual(self.order_item_admin.search_fields, expected_search_fields)
