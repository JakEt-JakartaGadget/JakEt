from django.urls import path
from Authenticate.views import *

app_name = 'Authenticate'

urlpatterns = [
    path('login/', log_in, name='login'),  
    path('register/', register, name='register'),  
    path('logout/', log_out, name='logout'),  
    path('login_app/', login_app, name='login_app'),  
    path('register_app/', register_app, name='register_app'),  
    path('logout_app/', logout_app, name='logout_app'),  
]
