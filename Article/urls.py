from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name='Article'

urlpatterns = [
    path('', article_list, name='article_list'),
    path('add/', add_article, name='add_article'),
    path('<int:pk>/', article_detail, name='article_detail'),
    path('edit/<int:pk>/', edit_article, name='edit_article'),
    path('delete/<int:pk>/', delete_article, name='delete_article'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
