from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex

class Phone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    image_url = models.URLField(max_length=500, blank=True, null=True)
    one_star = models.IntegerField(default=0)
    two_star = models.IntegerField(default=0)
    three_star = models.IntegerField(default=0)
    four_star = models.IntegerField(default=0)
    five_star = models.IntegerField(default=0)

    @property
    def avg_rating(self):
        total_ratings = (
            self.one_star + 
            self.two_star + 
            self.three_star + 
            self.four_star + 
            self.five_star
        )
        rating_sum = (
            1 * self.one_star + 
            2 * self.two_star + 
            3 * self.three_star + 
            4 * self.four_star + 
            5 * self.five_star
        )
        return rating_sum / total_ratings if total_ratings > 0 else 0

    @property
    def total_respondents(self):
        return (
            self.one_star + 
            self.two_star + 
            self.three_star + 
            self.four_star + 
            self.five_star
        )
    class Meta:
        indexes = [
            GinIndex(fields=['brand', 'model'])
        ]
    
