from django.urls import path
from .views import *

app_name = 'Dashboard'

urlpatterns = [
    path('',main_dashboard,name='main_dashboard'),
    path('edit/<uuid:product_id>/', edit_product, name='edit_product'),
    path('delete/<uuid:product_id>/', delete_product, name='delete_product'),
    path('add/', add_product, name='add_product'),
]