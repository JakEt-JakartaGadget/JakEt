from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_view, name='forum'),
    path('add-discussion/', views.add_discussion, name='add_discussion'),
    path('discussion/<uuid:discussion_id>/delete/', views.delete_discussion, name='delete_discussion'),
]
