from django.db import models
from django.contrib.auth.models import User
import uuid
from ServiceCenter.models import ServiceCenter

class Tiket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)
    service_date = models.DateField()
    service_time = models.TimeField()
    specific_problems = models.TextField(default="No specific problems mentioned")

    def __str__(self):
        return self.name
