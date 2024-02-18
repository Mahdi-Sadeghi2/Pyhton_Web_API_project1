from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"

class CartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.shopping_cart}"
