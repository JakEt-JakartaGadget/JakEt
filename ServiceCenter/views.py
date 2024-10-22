import datetime
from django.shortcuts import render, redirect, reverse
from ServiceCenter.forms import ServiceForm
from ServiceCenter.models import ServiceCenter
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import os
from jaket.settings import BASE_DIR


def show_service_page(request):
    dataset_path = os.path.join(BASE_DIR, 'dataset', 'service_center', 'service_centers.json')
    if not ServiceCenter.objects.exists():
        if os.path.exists(dataset_path):
            with open(dataset_path, 'r') as file:
                data = json.load(file)
                for entry in data:
                    ServiceCenter.objects.get_or_create(
                        name=entry['Name'],
                        defaults={
                            'address': entry['Address'],
                            'contact': entry['Contact'],
                            'rating': entry['Reviews'],
                            'total_reviews': entry['Total Reviews']
                        }
                    )

    context = { 
        'user': request.user.username,
        'last_login': request.COOKIES['last_login'],
        'service_centers': ServiceCenter.objects.all() 
    }

    return render(request, "service_page.html", context)

def create_service_center(request):
    form = ServiceForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        service_entry= form.save(commit=False)
        if request.user.is_authenticated:
            service_entry.user = request.user
        else:
            service_entry.user = None
        service_entry.save()
        return redirect('ServiceCenter:show_service_page')

    context = {'form': form}
    return render(request, "create_service_center.html", context)

@csrf_exempt
@require_POST
def add_service_center_ajax(request):
    name = request.POST.get("name")
    address = request.POST.get("address")
    contact = request.POST.get("contact")
    rating = request.POST.get("rating")
    total_reviews = request.POST.get("total_reviews")
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None 
        
    new_service_center = ServiceCenter(
        name=name, address=address,
        contact=contact, rating=rating, total_reviews=total_reviews,
        user=user
    )
    new_service_center.save()

    return HttpResponse(b"CREATED", status=201)

def edit_service_center(request, id):
    # Get service_center berdasarkan id
    service_center = ServiceCenter.objects.get(pk = id)

    form = ServiceForm(request.POST or None, instance=service_center)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('ServiceCenter:show_service_page'))

    context = {'form': form}
    return render(request, "edit_service_center.html", context)

def delete_service_center(request, id):
    # Get service center berdasarkan id
    service_center = ServiceCenter.objects.get(pk = id)
    # Hapus service center
    service_center.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('ServiceCenter:show_service_page'))


def show_xml(request):
    data = ServiceCenter.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ServiceCenter.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ServiceCenter.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ServiceCenter.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
