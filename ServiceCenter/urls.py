from django.urls import path
from ServiceCenter.views import show_service_page, create_service_center, edit_service_center, delete_service_center, add_service_center_ajax, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'ServiceCenter'

urlpatterns = [
    path('', show_service_page, name='show_service_page'),
    path('create-service-center', create_service_center, name='create_service_center'),
    path('create-ajax/', add_service_center_ajax, name='add_service_center_ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('edit-service-center/<uuid:id>', edit_service_center, name='edit_service_center'),
    path('delete-service-center/<uuid:id>', delete_service_center, name='delete_service_center'),
]

