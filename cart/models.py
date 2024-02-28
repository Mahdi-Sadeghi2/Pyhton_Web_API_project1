# models.py
from django.db import models
from store.models import User, Product


class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    cart_items = models.ManyToManyField(
        'CartItem', related_name='cart_items')  # Use a more descriptive name

    def __str__(self):
        return f"Cart - {self.customer.username if self.customer else 'Guest'} - Status: {self.status}"

    def archive_cart(self):
        self.status = 'archived'
        self.save()

    def add_item(self, item_data):
        product_id = item_data.get('product_id')
        quantity = item_data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)

            # Check if the item is already in the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=self, product=product)

            if not created:
                # Ensure quantity is always positive
                cart_item.quantity = max(1, cart_item.quantity + quantity)
            else:
                # Set the quantity if it's a new item
                cart_item.quantity = max(1, quantity)

            cart_item.save()  # Save the cart item
            self.cart_items.add(cart_item)  # Add the cart item to the cart

            # Save the updated cart
            self.save()

        except Product.DoesNotExist as error:
            # Handle the case where the item with the specified ID does not exist
            raise error

    def remove_item(self, product_id):
        try:
            product = Product.objects.get(id=product_id)

            # Check if the item is in the cart
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.delete()

            # Save the updated cart
            self.save()

        except (Product.DoesNotExist, CartItem.DoesNotExist) as error:
            # Handle the case where the product or item with the specified ID does not exist
            raise error

    def clear_cart(self):
        self.cart_items.all().delete()  # Clear cart items
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Ensure quantity is set to at least 1
        if self.quantity < 1:
            self.quantity = 1
        super().save(*args, **kwargs)
