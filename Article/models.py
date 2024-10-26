from django.db import models
from django.contrib.auth.models import User

class Artikel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='dataset/article_image', blank=True, null=True)
    source = models.CharField(max_length=100, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
