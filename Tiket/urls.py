from django.urls import path
from Tiket.views import create_tiket, reschedule_appointment, cancel_appointment, add_tiket_ajax, show_xml, show_json, show_xml_by_id, show_json_by_id
from ServiceCenter.views import show_service_page

app_name = 'Tiket'

urlpatterns = [
    path('', show_service_page, name='show_service_page'),
    path('create-tiket', create_tiket, name='create_tiket'),
    path('create-ajax/', add_tiket_ajax, name='add_tiket_ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('reschedule-appointment/<uuid:id>', reschedule_appointment, name='reschedule_appointment'),
    path('cancel-appointment/<uuid:id>', cancel_appointment, name='cancel_appointment'),
]

