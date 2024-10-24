from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
# from .forms import FirstDataForm, RegisterForm
from django.contrib.auth.models import User
from Authenticate.models import UserData
import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Phone
import uuid
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def home_section(request):
    phones = Phone.objects.all()
    context = {
        'phones': phones
    }
    return render(request, 'home.html', context)


@csrf_exempt
@login_required
def toggle_favorite(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Phone, id=product_id)
        product.is_favorite = not product.is_favorite
        product.save()
        return JsonResponse({'is_favorite': product.is_favorite})

@csrf_exempt
@login_required
def rate_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        rating = int(request.POST.get('rating'))
        product = get_object_or_404(Phone, id=product_id)
        product.rating = rating
        product.save()
        return JsonResponse({'success': True})
