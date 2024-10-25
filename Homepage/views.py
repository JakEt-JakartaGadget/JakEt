from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from Authenticate.models import UserData
import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Phone
import uuid
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from Wishlist.models import Favorite

def home_section(request):
    phones = Phone.objects.all()
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('phone_id', flat=True)
    context = {
        'phones': phones,
        'user_favorites': user_favorites 
    }
    return render(request, 'home.html', context)

def list_products(request):
    phones = Phone.objects.all()
    brands = Phone.objects.values_list('brand', flat=True).distinct()
    storages = Phone.objects.values_list('storage', flat=True).distinct()
    rams = Phone.objects.values_list('ram', flat=True).distinct()

    brand_filter = request.GET.get('brand')
    storage_filter = request.GET.get('storage')
    ram_filter = request.GET.get('ram')
    price_sort = request.GET.get('sort_price')

    if brand_filter:
        phones = phones.filter(brand=brand_filter)
    if storage_filter:
        phones = phones.filter(storage=storage_filter)
    if ram_filter:
        phones = phones.filter(ram=ram_filter)
    
    if price_sort == 'high_to_low':
        phones = phones.order_by('-price_inr')
    elif price_sort == 'low_to_high':
        phones = phones.order_by('price_inr')

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('phone_id', flat=True)

    context = {
        'phones': phones,
        'brands': brands,
        'storages': storages,
        'rams': rams,
        'user_favorites': user_favorites  # Pass this to the template
    }
    return render(request, 'list_product.html', context)


@csrf_exempt
@login_required(login_url='/authenticate/login')
def toggle_favorite(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, phone=phone)
    if not created:
        favorite.delete() 
        is_favorite = False
    else:
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})

@csrf_exempt
@login_required(login_url='/authenticate/login')
def rate_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        rating = int(request.POST.get('rating'))
        product = get_object_or_404(Phone, id=product_id)
        product.rating = rating
        product.save()
        return JsonResponse({'success': True})
