from django.urls import path
from .views import *

app_name = 'DetailProduct'

urlpatterns = [
    path('<uuid:product_id>/', product_detail, name='detail_page'),
    path('add_review/<uuid:product_id>/', add_review_ajax, name='add_review_ajax'),
    path('edit_review/', edit_review_ajax, name='edit_review_ajax'),  
    path('delete_review/<int:id>/', delete_review, name='delete_review'),
    path('reviews/<uuid:product_id>/', review_page, name='review_page'),
]
