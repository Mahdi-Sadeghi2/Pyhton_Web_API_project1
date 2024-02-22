from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('id',)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image_gallery = models.ManyToManyField('Image', related_name='product_images')
    video_gallery = models.ManyToManyField('Video', related_name='product_videos')
    user_comments = models.ManyToManyField('UserComment', related_name='product_comments', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('id',)    
    
    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='product_images/', blank=True)

class Video(models.Model):
    video = models.FileField(upload_to='product_videos/',null=True, blank=True)

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_user_comments')
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
