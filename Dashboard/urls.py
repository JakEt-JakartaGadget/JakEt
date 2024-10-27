from django.urls import path
from . import views

app_name = 'Dashboard'

urlpatterns = [
    path('customer-service/', views.chat_dashboard, name='chat_dashboard'),  #  Customer Service Dashboard
]