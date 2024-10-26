from django.urls import path
from .views import *

app_name = 'DetailProduct'

urlpatterns = [
    path('<uuid:product_id>/', product_detail, name='detail_page'),
    path('edit_review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('reviews/<uuid:product_id>/', review_page, name='review_page'),
]
