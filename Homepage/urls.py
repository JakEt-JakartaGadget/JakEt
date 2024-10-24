from django.urls import path
from .views import *

app_name = 'Homepage'

urlpatterns = [
    path('', home_section, name='home_section'),
]
