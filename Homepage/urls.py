from django.urls import path
from .views import *

app_name = 'Homepage'

urlpatterns = [
    path('', home_section, name='home_section'),
    path('toggle_favorite/<uuid:phone_id>/',toggle_favorite, name='toggle_favorite'),
    path('list_product/',list_products, name='list_product'),
    path('search_results/',search_results, name='search_results'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),
    path('json_allproduct/',show_json,name='show_json'),
    path('json_allproduct/<uuid:id>/', show_json_by_id, name='show_json_by_id'),
]
