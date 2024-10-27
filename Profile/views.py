from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db import IntegrityError
from Authenticate.models import UserData
from django.contrib.auth.models import User
from Profile.forms import ProfileForm

@login_required(login_url='/authenticate')
def profile_view(request):
    try:
        user_data = UserData.objects.get(user=request.user)
        context = {
            'profile_picture': user_data.profile_picture,
            'profile_name': user_data.profile_name,
            'username': user_data.username,
            'about': user_data.about,
            'phone': user_data.phone,
            'email': user_data.email,
            'user_data': user_data,
        }
        return render(request, 'profile.html', context)
    except UserData.DoesNotExist:
        return redirect('Profile:create_profile')

@login_required(login_url='/authenticate')
def create_profile(request):
    if UserData.objects.filter(user=request.user).exists():
        return redirect('Profile:profile_view')

    form = ProfileForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        profile_name = form.cleaned_data['profile_name']
        username = form.cleaned_data['username']
        about = form.cleaned_data['about']
        phone = form.cleaned_data['phone']
        email = form.cleaned_data['email']
        profile_picture = request.FILES.get('profile_picture')

        try:
            user = request.user
            user.username = username
            user.save()
            user_data = UserData.objects.create(
                user=request.user,
                profile_name=profile_name,
                username=username,
                about=about,
                phone=phone,
                email=email,
                profile_picture=profile_picture,
            )
            user_data.save()
            messages.success(request, "Profile created successfully!")
            return redirect('Profile:profile_view')
        except IntegrityError:
            messages.error(request, "An error occurred while creating the profile. Please try again.")

    return render(request, 'create_profile.html', {'form': form})

@login_required(login_url='/authenticate')
def edit_profile(request):
    profile = UserData.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'delete_picture' in request.POST:
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)
                profile.profile_picture = None
                profile.save()
                return JsonResponse({'status': 'success', 'message': 'Profile picture successfully deleted.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No profile picture to delete.'})

        if form.is_valid():
            new_username = form.cleaned_data['username']
            user = profile.user
            if user.username != new_username:
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, "Username already exists.")
                    return redirect('Profile:edit_profile')
                user.username = new_username

            form.save() 
            user.save()  

            messages.success(request, "Profile updated successfully!")
            return redirect(reverse('Profile:profile_view'))
        else:
            messages.error(request, "Profile update failed.")

    return render(request, 'edit_profile.html', {'form': form})


@login_required(login_url='/authenticate')
def delete_profile_picture(request):
    if request.method == "POST":
        profile = UserData.objects.get(user=request.user)
        if profile.profile_picture:
            profile.profile_picture.delete(save=True)
            profile.profile_picture = None
            profile.save()
            return JsonResponse({'message': 'Profile picture successfully deleted.'})
        else:
            return JsonResponse({'message': 'No profile picture to delete.'}, status=404)
    return JsonResponse({'message': 'Invalid request.'}, status=405)

def show_xml(request):
    data = UserData.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = UserData.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")