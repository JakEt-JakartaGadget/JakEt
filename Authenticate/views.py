from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import datetime
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse


def register(request):
    form = UserDataForm()
    if request.method == "POST":
        profile_name = request.POST['profile_name']
        username = request.POST['username']
        profile_picture = request.POST['url'] if request.POST['url'] != '' else None
        about = request.POST['about']
        location = request.POST['location']
        phone =  request.POST['phone']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        try:
            curruser = User.objects.get(username='username_yang_dicari') if username else None
        except Exception as e:
            curruser = None
        if pass1 != pass2:
            error_message = "Password yang dimasukkan tidak cocok. Silakan coba lagi."
            messages.info(request, error_message)
        elif curruser:
            error_message = "Username telah digunakan oleh pengguna lain."
            messages.info(request, error_message)
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            user_profile = UserData(user=user,profile_picture= profile_picture,fullname = fullname, username=username, age=age, country=country, city=city, password= password1)
            user_profile.save() 
            messages.success(request, 'Your account has been successfully created!')
            return redirect('/login')
    context = {'form':form}
    return render(request, 'register-next.html', context)

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("Homepage:home")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login-next.html', context)


def log_out(request):
    logout(request)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('last_login')
    return response

