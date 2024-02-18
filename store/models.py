from django.db import models

# Create your models here.
# store/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image_gallery = models.ManyToManyField('Image', related_name='product_images')
    video_gallery = models.ManyToManyField('Video', related_name='product_videos')
    user_comments = models.ManyToManyField('UserComment', related_name='product_comments')

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')

class Video(models.Model):
    video = models.FileField(upload_to='product_videos/')

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment_text = models.TextField()
    enabled = models.BooleanField(default=False)
    approved_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.comment_text}"
