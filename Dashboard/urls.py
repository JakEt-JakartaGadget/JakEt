from django.urls import path
from Dashboard.views import dashboard_tiket, cancel_appointment, create_service_center, edit_service_center, delete_service_center, dashboard_service

app_name = 'Dashboard'

urlpatterns = [
    path('tiket/', dashboard_tiket, name='dashboard_tiket'),
    path('cancel-appointment/<uuid:id>/', cancel_appointment, name='cancel_appointment'),
    path('create-service-center/', create_service_center, name='create_service_center'),
    path('edit-service-center/<uuid:id>/', edit_service_center, name='edit_service_center'),
    path('delete-service-center/<uuid:id>/', delete_service_center, name='delete_service_center'),
    path('service/', dashboard_service, name='dashboard_service'),
]
