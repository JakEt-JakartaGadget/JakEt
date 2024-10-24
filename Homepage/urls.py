from django.urls import path
from .views import *

app_name = 'Homepage'

urlpatterns = [
    path('', home_section, name='home_section'),
    # path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
    # path('rate-product/', rate_product, name='rate_product'),
]
