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
