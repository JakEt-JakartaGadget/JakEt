import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.DateTimeField(auto_now_add=True)
    topic = models.TextField()
    # Remove the last_reply field from here
    
    @property
    def last_reply(self):
        return self.reply_set.order_by('-date', '-time_sent').first()

class Reply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)  # Renamed from discussion_id
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    message = models.TextField()
    time_sent = models.TimeField(auto_now_add=True)