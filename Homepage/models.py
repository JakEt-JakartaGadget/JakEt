from django.db import models
import uuid
from django.contrib.auth.models import User

class Phone(models.Model):
    id = models.UUIDField(primary_key=True,default = uuid.uuid4, editable=False)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=255)
    storage = models.CharField(max_length=50)  
    ram = models.CharField(max_length=50)      
    screen_size_inches = models.FloatField()    
    camera_mp = models.CharField(max_length=100)  
    battery_capacity_mAh = models.IntegerField()   
    price_usd = models.DecimalField(max_digits=10, decimal_places=2) 
    price_inr = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    rating = models.IntegerField(default=0) 
    is_favorite = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
class PhoneRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'phone')
