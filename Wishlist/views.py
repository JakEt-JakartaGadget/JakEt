from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from Homepage.models import Phone  
from .models import Favorite  

@login_required(login_url='/authenticate/login')
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'favorites': favorites})

@login_required(login_url='/authenticate/login')
def remove_favorite(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    favorite = Favorite.objects.filter(user=request.user, phone=phone)
    if favorite.exists():
        favorite.delete()
    return redirect('Wishlist:favorite_list')