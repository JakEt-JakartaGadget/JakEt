from django.db import models
from django.contrib.auth.models import User
import uuid

class ServiceCenter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_reviews = models.IntegerField()

    def __str__(self):
        return self.name
