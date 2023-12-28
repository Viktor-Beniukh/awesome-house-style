from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from goods.models import Product

from users.models import User


class OrderItemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    NEW = "New"
    INPROCESSING = "In processing"
    SHIPPED = "Shipped"
    RECEIVED = "Received"

    STATUS_ORDER = (
        (NEW, "New"),
        (INPROCESSING, "In processing"),
        (SHIPPED, "Shipped"),
        (RECEIVED, "Received"),
    )

    user = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None
    )
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    zipcode = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    requires_delivery = models.BooleanField(default=False)
    payment_on_get = models.BooleanField(default=False)
    status_order = models.CharField(max_length=20, choices=STATUS_ORDER, default=NEW)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order № {self.pk} | Consumer {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(
        to=Product, on_delete=models.SET_DEFAULT, null=True, related_name="order_items", default=None
    )
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OrderItemQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f'Product "{self.name}" | Order № {self.order.pk}'
