from django.urls import path
from . import views

app_name = 'CustomerService'

urlpatterns = [
    path('<int:user_id>/', views.customer_service, name='customer_service_for_user'),
    path('<int:user_id>/send/', views.send_message, name='send_message'),
    path('messages/', views.get_messages, name='get_messages'),
    path('json/', views.show_json, name='show_json'),
    path('send_message_flutter/', views.send_message_flutter, name='send_message_flutter'),
]