from django.shortcuts import render, redirect, reverse
from Authenticate.models import UserData
from Profile.forms import ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/authenticate')
def profile_view(request):
    try:
        # Mendapatkan data profil pengguna yang sedang login
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

def create_profile(request):
    if request.method == 'POST':
        print("Received POST data:", request.POST)
        profile_name = request.POST.get('profile_name')
        username = request.POST.get('username')
        about = request.POST.get('about')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')

        # Membuat user baru dengan password dari form
        user = User.objects.create_user(username=username)

        # Simpan data profil
        user_data = UserData(
            user=user,
            profile_name=profile_name,
            username=username,
            about=about,
            phone=phone,
            email=email,
            profile_picture=profile_picture,
        )
        user_data.save()

        return redirect('Profile:profile_view')

    return render(request, 'create_profile.html')

@login_required(login_url='/authenticate')
def edit_profile(request):
    # Mendapatkan profil pengguna yang sedang login
    profile = UserData.objects.get(user=request.user)

    if request.method == "POST":
        # Jika tombol "Delete Picture" diklik
        if 'delete_picture' in request.POST:
            # Menghapus gambar profil
            profile.profile_picture.delete(save=True)
            profile.profile_picture = None  # Atur gambar profil menjadi None
            profile.save()  # Simpan perubahan
            return HttpResponseRedirect(reverse('profile_view'))

        # Jika form untuk mengganti atau menyimpan profil di-submit
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile_view'))

    else:
        form = ProfileForm(instance=profile)  # Form diisi dengan data pengguna yang ada

    context = {'form': form}
    return render(request, "edit_profile.html", context)

def show_xml(request):
    data = UserData.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = UserData.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
