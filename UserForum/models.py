import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.DateTimeField(auto_now_add=True)
    topic = models.TextField()
    
    @property
    def reply_set(self):
        return Reply.objects.filter(Discussion=self).order_by('-replied')

    @property
    def last_reply(self):
        if self.reply_set:
            return self.reply_set.first()
        return None

class Reply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    replied = models.DateTimeField(default=timezone.now)
    message = models.TextField()