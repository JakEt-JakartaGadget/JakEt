import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    message = models.TextField()
    time_sent = models.TimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.read = True
        self.save()

class DailyCustomerService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    @property
    def messages(self):
        return Chat.objects.filter(date=self.date, user=self.user)