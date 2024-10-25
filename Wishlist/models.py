from django.db import models
from django.contrib.auth.models import User
from Homepage.models import Phone  

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)  

    class Meta:
        unique_together = ('user', 'phone') 

    def __str__(self):
        return f"{self.user.username} - {self.phone.model}"