from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.content
        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(
            upload_to='posts/images',
            processors=[ResizeToFill(600, 600)],
            format='JPEG',
            options={'quality': 100},)