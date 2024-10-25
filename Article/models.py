from django.db import models

class Artikel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/', default='article_images/default.png')
    source = models.CharField(max_length=100, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
