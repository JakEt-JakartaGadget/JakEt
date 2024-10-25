from django.urls import path
from .views import *

app_name = 'DetailProduct'

urlpatterns = [
    path('', detail_page, name='detail_page'),
]
