from django.urls import path
from . import views

app_name='UserForum'

urlpatterns = [
    path('', views.forum_view, name='forum'),
    path('add-discussion/', views.add_discussion, name='add_discussion'),
    path('discussion/<uuid:discussion_id>/delete/', views.delete_discussion, name='delete_discussion'),
    path('discussion/<uuid:id>/', views.discussion_view, name='discussion_view'),
    path('discussion/<uuid:id>/send/', views.send_reply, name='send_reply'),
    path('json/', views.show_json, name='show_json'),
    path('get-reply/<uuid:id>/', views.get_replies, name='get_replies'),
    path('add-discussion-flutter/', views.add_discussion_flutter, name='add_discussion_flutter'),
    path('send-reply-flutter/', views.send_reply_flutter, name='send_reply_flutter'),
]