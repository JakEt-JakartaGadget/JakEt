from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from Homepage.models import Phone  
from .models import Favorite  
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def show_wishlist_json(request):
    if not request.user.is_authenticated:
        print("User not authenticated")
        return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)
    
    print("User authenticated")
    phone_ids = Favorite.objects.filter(user=request.user).values_list('phone_id', flat=True)
    data = Phone.objects.filter(id__in=phone_ids)
    return HttpResponse(serializers.serialize("json", data), content_type='application/json')


@csrf_exempt
@login_required(login_url='/login')  
def add_to_favorite_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_id = data.get("phone_id")
        if phone_id is None:
            return JsonResponse({"status": "error", "message": "No phone_id provided"}, status=400)

        try:
            phone = Phone.objects.get(id=phone_id)
        except Phone.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Phone not found"}, status=404)

        favorite, created = Favorite.objects.get_or_create(user=request.user, phone=phone)

        if created:
            return JsonResponse({"status": "success", "message": "Added to favorites"}, status=200)
        else:
            return JsonResponse({"status": "info", "message": "Already in favorites"}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
@csrf_exempt
def remove_from_favorite(request, phone_id):
    if request.method == 'DELETE':
        try:
            phone = Phone.objects.get(id=phone_id)
        except Phone.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Phone not found"}, status=404)

        favorite = Favorite.objects.filter(user=request.user, phone=phone)
        if favorite.exists():
            favorite.delete()
            return JsonResponse({"status": "success", "message": "Removed from favorites"}, status=200)
        else:
            return JsonResponse({"status": "info", "message": "Not in favorites"}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
