from django.urls import path
from . import views

app_name = 'CustomerService'

urlpatterns = [
    path('', views.customer_service, name='customer_service'),
    path('send/', views.send_message, name='send_message'),
    path('messages/', views.get_messages, name='get_messages'),
]