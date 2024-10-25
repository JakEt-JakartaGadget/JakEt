from django.urls import path
from .views import *

app_name = 'Homepage'

urlpatterns = [
    path('', home_section, name='home_section'),
    path('toggle_favorite/',toggle_favorite, name='toggle_favorite'),
    path('rate_product/',rate_product, name='rate_product'),
    path('list_product/',list_products, name='list_product'),
]
