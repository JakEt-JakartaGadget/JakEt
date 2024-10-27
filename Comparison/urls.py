from django.urls import path
from Comparison.views import comparison_view

app_name = 'Comparison'

urlpatterns = [
    path('', comparison_view, name='comparison'),
]
