"""
URL configuration for jaket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Homepage.urls')),
    path('article/', include('Article.urls')),
    path('comparison/', include('Comparison.urls')),
    path('customerservice/', include('CustomerService.urls')),
    path('dashboard/', include('Dashboard.urls')),
    path('detailproduct/', include('DetailProduct.urls')),
    path('profile/', include('Profile.urls')),
    path('review/', include('Review.urls')),
    path('servicecenter/', include('ServiceCenter.urls')),
    path('tiket/', include('Tiket.urls')),
    path('userforum/', include('UserForum.urls')),
    path('wishlist/', include('Wishlist.urls')),
]
