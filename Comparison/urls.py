from django.urls import path
from Comparison.views import comparison_view, get_devices_from_csv, compare_devices

app_name = 'Comparison'

urlpatterns = [
    path('', comparison_view, name='comparison'),
    path('devices/', get_devices_from_csv, name='get_devices_from_csv'),
    path('compare/', compare_devices, name='compare_devices'),
]
