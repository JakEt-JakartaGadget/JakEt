from django.urls import path
from .views import *

app_name = 'Wishlist'

urlpatterns = [
    path('', favorite_list_web, name='favorite_list'), 
    path('remove/<uuid:phone_id>/', remove_favorite_web, name='remove_favorite'),
    path('wish_json/', show_wishlist_json, name='show_wishlist_json'),
    path('remove_from_favorite_flutter/', remove_from_favorite_flutter, name='remove_flutter'),
    path('add_to_favorite_flutter/', add_to_favorite_flutter, name='add_to_favorite_flutter'),
    ]