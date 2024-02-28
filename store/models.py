from django.db import models
from django.contrib.auth.models import User




class Category(models.Model):
    # Represents a category for products
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Price(models.Model):
    # Represents the price of a product with amount, currency, and activation status
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.amount} {self.currency}"


class Media(models.Model):
    # Represents media associated with a product (image or video)
    media_type = (('image', 'Image'), ('video', 'Video'),)
    media = models.CharField(
        max_length=10, choices=media_type, null=True, blank=True)
    file = models.FileField(blank=True, null=True)


class Product(models.Model):
    # Represents a product with name, category, description, media, user comments, and price
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    media = models.ForeignKey(
        Media, on_delete=models.CASCADE, null=True, blank=True)
    user_comments = models.ManyToManyField(
        'UserComment', related_name='product_comments', blank=True)
    price_item = models.ForeignKey(
        Price, related_name='prices', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def price_items(self):
        # Returns the active price for the product
        return self.price_item.filter(is_active=True).last()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('id',)

    def __str__(self):
        return self.name


class UserComment(models.Model):
    # Represents a user comment on a product
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='store_user_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    approved_by_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Comment'
        verbose_name_plural = 'User Comments'
        ordering = ('id',)

    def __str__(self):
        return f"{self.user.username} - {self.comment_text}"
