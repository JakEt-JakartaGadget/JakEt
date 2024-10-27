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
    sent_by_user = models.BooleanField(default=True)

    @classmethod
    def count_unread_messages(cls, user):
        return cls.objects.filter(user=user, read=False).count()

    def mark_as_read(self):
        self.read = True
        self.save()

class DailyCustomerService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    @property
    def messages(self):
        # Fetch messages for this user on the same date
        return Chat.objects.filter(date=self.date, user=self.user).order_by('time_sent')
