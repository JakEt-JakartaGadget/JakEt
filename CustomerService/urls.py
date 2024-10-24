from django.urls import path
from . import views

app_name = 'CustomerService'

urlpatterns = [
    path('chat/', views.customer_service, name='customer_service'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/messages/', views.get_messages, name='get_messages'),
]