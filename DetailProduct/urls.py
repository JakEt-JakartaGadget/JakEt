from django.urls import path
from .views import *

app_name = 'DetailProduct'

urlpatterns = [
    path('<uuid:product_id>/', product_detail, name='detail_page'),
    path('edit_review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('reviews/<uuid:product_id>/', review_page, name='review_page'),
    path('create_review_flutter/', create_review_flutter, name='create_review_flutter'),
    path('edit_review_flutter/<int:review_id>/', edit_review_flutter, name='edit_review_flutter'),
    path('delete_review_flutter/<int:review_id>/', delete_review_flutter, name='delete_review_flutter'),
    path('list_review/<uuid:product_id>/', list_reviews_flutter, name='list_reviews_flutter'),
]
