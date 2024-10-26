from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_view, name='forum'),
    path('add-discussion/', views.add_discussion, name='add_discussion'),
    path('discussion/<uuid:discussion_id>/delete/', views.delete_discussion, name='delete_discussion'),
    path('discussion/<uuid:id>/', views.discussion_view, name='discussion_view'),
    path('discussion/<uuid:id>/send/', views.send_reply, name='send_reply'),
]