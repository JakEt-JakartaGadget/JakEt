from django.db import models
from django.contrib.auth.models import User
from Homepage.models import *

class UserData(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='auth')
    favorite_phones = models.ManyToManyField(Phone, blank=True, related_name='favorited_by')
    profile_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    profile_picture = models.TextField(blank=True,null=True)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15,blank=True,null=True)
    email = models.CharField(max_length=50,blank=True,null=True)
    password = models.CharField(max_length=255,blank=False,null=False)
    


    def lst_data(self):
        dct = {
            'id' : self.user.pk,
            'profile_name' : self.profile_name,
            'username' : self.username,
            'profile_picture': self.profile_picture,
            'about' : self.about,
            'location' : self.location,
            'phone' : self.phone,
            'email' : self.email,
        }
        return dct



