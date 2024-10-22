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

@csrf_exempt
def home_section(request):
    context={}
    return render(request,'home.html',context)