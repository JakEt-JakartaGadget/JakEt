from django.db import models
import uuid

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
    price_inr = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Contoh: 999 * 15600 = 15,600,000

    def __str__(self):
        return f"{self.brand} {self.model}"
