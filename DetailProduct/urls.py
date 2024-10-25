from django.urls import path
from .views import *

app_name = 'DetailProduct'

urlpatterns = [
    path('<uuid:product_id>/', product_detail, name='detail_page'),
    path('<uuid:product_id>/submit_review/', submit_review, name='submit_review'),
    path('<uuid:product_id>/toggle_favorite/', toggle_favorite, name='toggle_favorite'),
    path('<uuid:product_id>/rate_product/', rate_product, name='rate_product'),
    path('review/<int:review_id>/edit/', edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', delete_review, name='delete_review'),
]
