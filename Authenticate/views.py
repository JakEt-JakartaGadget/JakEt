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
# @login_required
# def first_time_login(request):
#     # Periksa apakah pengguna sudah memiliki profil
#     try:
#         user_profile = UserData.objects.get(user=request.user)
#         return redirect('Homepage:home')  
#     except UserData.DoesNotExist:
#         # Jika belum ada profil, minta user melengkapi form
#         if request.method == 'POST':
#             form = FirstDataForm(request.POST, request.FILES)
#             if form.is_valid():
#                 user_profile = form.save(commit=False)
#                 user_profile.user = request.user
#                 user_profile.save()
#                 return redirect('Homepage:home')  
#         else:
#             form = FirstDataForm()
        
#         return render(request, 'first_time_login.html', {'form': form})

# def register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         pass1 = request.POST['password1']
#         pass2 = request.POST['password2']

#         if pass1 != pass2:
#             messages.error(request, "Password yang dimasukkan tidak cocok. Silakan coba lagi.")
#         elif User.objects.filter(username=username).exists():
#             messages.error(request, "Username telah digunakan oleh pengguna lain.")
#         else:
#             user = User.objects.create_user(username=username, password=pass1)
#             user.save()
#             messages.success(request, 'Akun Anda berhasil dibuat! Silakan login.')
#             return redirect('Authenticate:login') 

#     return render(request, 'register.html')

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
            # Jika user belum melengkapi profil, redirect ke first_time_login
            # if not UserData.objects.filter(user=user).exists():
            #     return redirect('first_time_login')  
            
            response = HttpResponseRedirect(reverse("Homepage:home_section")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))  
            return response
        else:
            messages.error(request, 'Username atau password salah. Silakan coba lagi.')
    
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    response = HttpResponseRedirect(reverse('Authenticate:login'))  
    response.delete_cookie('last_login')  
    return response
