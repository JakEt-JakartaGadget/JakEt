from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Homepage.models import Phone
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    product = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='product_reviews')
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.rating}/5 for {self.product}"