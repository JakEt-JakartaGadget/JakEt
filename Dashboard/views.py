from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from ServiceCenter.models import ServiceCenter
from Tiket.models import Tiket
from ServiceCenter.forms import ServiceForm
from Authenticate.models import UserData

def dashboard_tiket(request):
    users = UserData.objects.prefetch_related('tiket_set').all()
    users_with_appointments = []

    for user in users:
        user_appointments = user.tiket_set.all()
        if user_appointments:
            users_with_appointments.append({
                'user': user.user,
                'appointments': user_appointments
            })
    
    return render(request, 'dashboard_tiket.html', {'users': users_with_appointments})


def cancel_appointment(request, id):
    tiket = get_object_or_404(Tiket, pk=id)
    tiket.delete()
    return HttpResponseRedirect(reverse('Dashboard:dashboard_tiket'))

def dashboard_service(request):
    service_centers = ServiceCenter.objects.all()
    return render(request, 'dashboard_service.html', {'service_centers': service_centers})

def create_service_center(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service_entry = form.save(commit=False)
            if request.user.is_authenticated:
                user_data = UserData.objects.get(user=request.user)
                service_entry.user = user_data
            service_entry.save()
            return redirect('Dashboard:dashboard_service')
    else:
        form = ServiceForm()
    return render(request, "create_service_center.html", {'form': form})

def edit_service_center(request, id):
    service_center = get_object_or_404(ServiceCenter, pk=id)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=service_center)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('Dashboard:dashboard_service'))
    return render(request, "edit_service_center.html", {'form': form})

def delete_service_center(request, id):
    service_center = get_object_or_404(ServiceCenter, pk=id)
    service_center.delete()
    return HttpResponseRedirect(reverse('Dashboard:dashboard_service'))
