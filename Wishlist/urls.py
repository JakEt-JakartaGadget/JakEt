from django.urls import path
from .views import remove_favorite, favorite_list

app_name = 'Wishlist'

urlpatterns = [
    path('', favorite_list, name='favorite_list'), 
    path('remove/<uuid:phone_id>/', remove_favorite, name='remove_favorite'),]