from django.db import models
import uuid

class Gadget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    picture_url = models.URLField(max_length=500)
    battery_capacity_mAh = models.IntegerField()
    price_inr = models.CharField(max_length=100)
    ram = models.CharField(max_length=50)
    camera = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)  
    screen_size = models.CharField(max_length=100)  
    url = models.URLField(max_length=500)  

    def __str__(self):
        return f'{self.product_name} - {self.model}'
