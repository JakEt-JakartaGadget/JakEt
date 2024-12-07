from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .forms import FirstDataForm, RegisterForm
from django.contrib.auth.models import User
from .models import UserData
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

'''
DJANGO WEB AUTHENTICATION
'''
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username telah digunakan oleh pengguna lain.")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Akun Anda berhasil dibuat! Silakan login.')
                return redirect('Authenticate:login')
        else:
            messages.error(request, "Form tidak valid. Silakan cek kembali.")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)   
            if user.is_staff:
                response = HttpResponseRedirect(reverse("Dashboard:main_dashboard"))
                response.set_cookie('last_login', str(datetime.datetime.now()))  
                return response

            response = HttpResponseRedirect(reverse("Homepage:home_section")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))  
            return response
        else:
            messages.error(request, 'Username atau password salah. Silakan coba lagi.')
    
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    response = HttpResponseRedirect(reverse('Homepage:home_section'))  
    response.delete_cookie('last_login')  
    return response

'''
FLUTTER APP AUTHENTICATION
'''

@csrf_exempt
def register_app(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Method not allowed. Use POST."
        }, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status": False,
            "message": "Invalid JSON."
        }, status=400)

    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if not username or not password1 or not password2:
        return JsonResponse({
            "status": False,
            "message": "All fields are required."
        }, status=400)

    if password1 != password2:
        return JsonResponse({
            "status": False,
            "message": "Passwords do not match."
        }, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "status": False,
            "message": "Username already exists."
        }, status=400)

    try:
        user = User.objects.create_user(username=username, password=password1)
        user.save()
    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": "Error creating user."
        }, status=500)

    return JsonResponse({
        "username": user.username,
        "status": True,
        "message": "User created successfully!"
    }, status=201)


@csrf_exempt
def login_app(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Method not allowed. Use POST."
        }, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status": False,
            "message": "Invalid JSON."
        }, status=400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({
            "status": False,
            "message": "Username and password are required."
        }, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account is deactivated."
            }, status=403)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, please check your username or password."
        }, status=401)


@csrf_exempt
def logout_app(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Method not allowed. Use POST."
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "status": False,
            "message": "User is not authenticated."
        }, status=401)

    try:
        username = request.user.username
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout successful!"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=500)

