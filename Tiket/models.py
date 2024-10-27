from django.db import models
from Authenticate.models import UserData
import uuid
from ServiceCenter.models import ServiceCenter

class Tiket(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)
    service_date = models.DateField()
    service_time = models.TimeField()
    specific_problems = models.TextField(default="No specific problems mentioned")

    def __str__(self):
        user_name = self.user.user if self.user else self.user
        return f"{user_name} - {self.service_center.name} - {self.service_date}"
