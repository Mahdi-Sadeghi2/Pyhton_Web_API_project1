from django.db import models
from django.contrib.auth.models import User

class ContentCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE)
    description = models.TextField()
    image_gallery = models.ManyToManyField('Image', related_name='content_images')
    video_gallery = models.ManyToManyField('Video', related_name='content_videos')
    user_comments = models.ManyToManyField('UserComment', related_name='content_comments', blank=True, default=None)
    
    class Meta:
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'
        ordering = ('id',)
    
    def __str__(self):
        return self.title

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

class Video(models.Model):
    video = models.FileField(upload_to='videos/')

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_user_comments')
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    comment_text = models.TextField()
    enabled = models.BooleanField(default=False)
    approved_by_admin = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'UserComment'
        verbose_name_plural = 'UserComments'
        ordering = ('id',)

    def __str__(self):
        return f"{self.user.username} - {self.comment_text}"

    