from django.db import models

# Create your models here.
# financial/models.py
from django.db import models
from cart.models import ShoppingCart
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failure', 'Failure')])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_status}"
