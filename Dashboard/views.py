# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from Homepage.models import Phone
from Homepage.forms import PhoneForm

@staff_member_required(login_url='/authenticate/login')
def main_dashboard(request):
    products = Phone.objects.all().order_by('-id')
    context = {
        'products': products,
        'title': 'Product Dashboard'
    }
    return render(request, 'dashboard.html', context)

@staff_member_required(login_url='/authenticate/login')
def add_product(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('Dashboard:main_dashboard')
    else:
        form = PhoneForm()
    
    context = {
        'form': form,
        'title': 'Add New Product',
        'submit_text': 'Add Product'
    }
    return render(request, 'product_form.html', context)

@staff_member_required(login_url='/authenticate/login')
def edit_product(request, product_id):
    product = get_object_or_404(Phone, pk=product_id)
    
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('Dashboard:main_dashboard')
    else:
        form = PhoneForm(instance=product)
    
    context = {
        'form': form,
        'title': f'Edit Product: {product.brand} {product.model}',
        'submit_text': 'Update Product'
    }
    return render(request, 'product_form.html', context)

@staff_member_required(login_url='/authenticate/login')
def delete_product(request, product_id):
    product = get_object_or_404(Phone, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('Dashboard:main_dashboard')