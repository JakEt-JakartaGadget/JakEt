import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from Tiket.forms import TiketForm
from Tiket.models import Tiket
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST
from ServiceCenter.models import ServiceCenter
from Authenticate.models import UserData


def create_tiket(request, id):
    service_center = get_object_or_404(ServiceCenter, pk=id)
    if request.method == "POST":
        form = TiketForm(request.POST)
        form.request = request
        if form.is_valid():
            tiket = form.save(commit=False)
            if request.user.is_authenticated:
                user, created = UserData.objects.get_or_create(user=request.user) 
                tiket.user = user
            else:
                tiket.user = None
            tiket.save()
            return redirect('ServiceCenter:show_service_page')
    else:
        form = TiketForm(initial={'service_center': service_center})
    context = {'form': form, 'service_center': service_center}
    return render(request, "make_appointment.html", context)



def reschedule_appointment(request, id):
    # Get tiket berdasarkan id
    tiket = get_object_or_404(Tiket, pk=id)
    if request.method == "POST":
        form = TiketForm(request.POST, instance=tiket, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ServiceCenter:show_service_page'))
    else:
        form = TiketForm(instance=tiket, request=request)

    context = {'form': form}
    return render(request, "reschedule_appointment.html", context)


def cancel_appointment(request, id):
    tiket = Tiket.objects.get(pk=id)
    
    if request.method == "POST":
        tiket.delete()
        return HttpResponseRedirect(reverse('ServiceCenter:show_service_page'))
    
    return render(request, 'confirm_cancel.html', {'tiket': tiket})


def show_xml(request):
    data = Tiket.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    if request.user.is_authenticated:
        user_data = UserData.objects.get(user=request.user)
        data = Tiket.objects.filter(user=user_data).select_related('service_center')
        tiket_list = []
        for tiket in data:
            tiket_dict = {
                'id': str(tiket.id),
                'service_date': tiket.service_date,
                'service_time': tiket.service_time,
                'specific_problems': tiket.specific_problems,
                'service_center': {
                    'name': tiket.service_center.name,
                    'address': tiket.service_center.address,
                    'contact': tiket.service_center.contact,
                },
            }
            tiket_list.append(tiket_dict)
        return JsonResponse(tiket_list, safe=False)
    else:
        return JsonResponse([], safe=False)


def show_xml_by_id(request, id):
    data = Tiket.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Tiket.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
