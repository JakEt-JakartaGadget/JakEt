from django.urls import path
from .views import *

app_name = 'Dashboard'

urlpatterns = [
    path('',main_dashboard,name='main_dashboard'),
    path('edit/<uuid:product_id>/', edit_product, name='edit_product'),
    path('delete/<uuid:product_id>/', delete_product, name='delete_product'),
    path('add/', add_product, name='add_product'),
    path('tiket/', dashboard_tiket, name='dashboard_tiket'),
    path('cancel-appointment/<uuid:id>/', cancel_appointment, name='cancel_appointment'),
    path('create-service-center/', create_service_center, name='create_service_center'),
    path('edit-service-center/<uuid:id>/', edit_service_center, name='edit_service_center'),
    path('delete-service-center/<uuid:id>/', delete_service_center, name='delete_service_center'),
    path('service/', dashboard_service, name='dashboard_service'),
    path('customer-service/', chat_dashboard, name='chat_dashboard'), 
]