from django.urls import path, include
from Profile.views import (
    profile_view,
    edit_profile,
    create_profile,
    delete_profile_picture,
    show_xml,
    show_json,
    create_profile_flutter,
    edit_profile_flutter,
)
from Authenticate.views import log_in
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Profile'

urlpatterns = [
    path('login/', log_in, name='login'),
    path('', profile_view, name='profile_view'),
    path('create-profile/', create_profile, name='create_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-picture/', delete_profile_picture, name='delete_profile_picture'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('create-flutter/', create_profile_flutter, name='create_profile_flutter'),
    path('edit-flutter/', edit_profile_flutter, name='edit_profile_flutter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)