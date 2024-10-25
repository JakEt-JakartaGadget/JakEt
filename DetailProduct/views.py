from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from Authenticate.models import UserData
import datetime
from django.views.decorators.csrf import csrf_exempt
from Homepage.models import Phone
import uuid
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required(login_url='/authenticate/login')
def detail_page(request):
    context = {}
    return render(request,'detail.html',context)
