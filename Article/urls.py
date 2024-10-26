from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('add/', views.add_article, name='add_article'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('edit/<int:pk>/', views.edit_article, name='edit_article'),
    path('delete/<int:pk>/', views.delete_article, name='delete_article'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
