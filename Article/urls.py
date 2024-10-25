from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('artikels/', views.artikel_list, name='artikel_list'),
    path('artikels/<int:pk>/', views.artikel_detail, name='artikel_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)