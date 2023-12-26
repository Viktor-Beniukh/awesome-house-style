from django.db import models

from goods.models import Product
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartQueryset().as_manager()

    def __str__(self):
        if self.user:
            return f"Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity}"
        return f"Anonym cart | Product {self.product.name} | Quantity {self.quantity}"

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)
