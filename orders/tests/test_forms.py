from django.contrib.auth import get_user_model
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.test import TestCase

from orders.forms import CreateOrderForm

User = get_user_model()


class OrderCreateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="john.doe@example.com",
            password="testpassword")
        self.client.force_login(self.user)

    def test_create_order_form_valid_data(self):

        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+987654321023",
            "requires_delivery": "1",
            "shipping_address": "123 Main St",
            "city": "City",
            "country": "Country",
            "zipcode": 12345,
            "payment_on_get": "1",
        }
        form = CreateOrderForm(data=form_data)

        self.assertTrue(form.is_valid(), form.errors)

    def test_create_order_form_invalid_data(self):
        form_data = {
            "first_name": "John",
        }

        form = CreateOrderForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_create_order_form_field_types(self):
        form = CreateOrderForm()

        self.assertIsInstance(form.fields["first_name"], forms.CharField)
        self.assertIsInstance(form.fields["last_name"], forms.CharField)
        self.assertIsInstance(form.fields["email"], forms.EmailField)
        self.assertIsInstance(form.fields["phone_number"], PhoneNumberField)
        self.assertIsInstance(form.fields["requires_delivery"], forms.ChoiceField)
        self.assertIsInstance(form.fields["shipping_address"], forms.CharField)
        self.assertIsInstance(form.fields["city"], forms.CharField)
        self.assertIsInstance(form.fields["country"], forms.CharField)
        self.assertIsInstance(form.fields["zipcode"], forms.IntegerField)
        self.assertIsInstance(form.fields["payment_on_get"], forms.ChoiceField)
