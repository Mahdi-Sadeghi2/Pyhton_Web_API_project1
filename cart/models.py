from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'shopping Cart'
        verbose_name_plural = 'shopping Carts'
        ordering = ('id',)
    
    def __str__(self):
        return f"Shopping Cart for {self.user.username}"

class CartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        ordering = ('id',)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.shopping_cart}"
