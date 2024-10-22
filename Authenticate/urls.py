from django.urls import path
from Authenticate.views import *

app_name = 'Authenticate'

urlpatterns=[
    path('login/',log_in,name='login'),
    path('register/',register,name='register'),
    path('logout/',log_out,name='logout'),
    path('',log_in,name='login'),
]