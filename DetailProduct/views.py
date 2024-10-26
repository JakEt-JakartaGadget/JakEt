from datetime import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from DetailProduct.forms import ReviewForm
from Homepage.models import Phone
from .models import Review
import json
from django.db.models import Avg
from Wishlist.models import Favorite
from collections import defaultdict
from django.contrib import messages
from django.utils import timezone

@login_required(login_url='/authenticate/login')
def product_detail(request, product_id):
    product = get_object_or_404(Phone, id=product_id)
    reviews = Review.objects.filter(product=product)
    user_has_review = reviews.filter(user=request.user).exists()
    user_review = reviews.filter(user=request.user).first() if user_has_review else None
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('phone_id', flat=True)
    star_counts = [
        (5, product.five_star),
        (4, product.four_star),
        (3, product.three_star),
        (2, product.two_star),
        (1, product.one_star),
    ]
    
    context = {
        'product': product,
        'reviews': reviews,
        'user_has_review': user_has_review,
        'user_review': user_review,
        'user_favorites': user_favorites,  
        'star_counts': star_counts, 
    }
    return render(request, 'detail.html', context)

@csrf_exempt
@login_required(login_url='/authenticate/login')
def toggle_favorite(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, phone=phone)
    if not created:
        favorite.delete() 
        is_favorite = False
    else:
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})

@login_required(login_url='/authenticate/login')
def review_page(request, product_id):
    product = get_object_or_404(Phone, id=product_id)
    user_reviews = Review.objects.filter(product=product)
    form = ReviewForm(request.POST or None)
    review_counts = defaultdict(int)
    user_has_reviewed = Review.objects.filter(product=product, user=request.user).exists()
    
    for review in user_reviews:
        review_counts[review.rating] += 1

    if request.method == 'POST':
        if form.is_valid():
            if user_has_reviewed:
                messages.error(request, "Anda sudah memberikan review untuk produk ini")
                return redirect('DetailProduct:review_page', product_id=product_id)
            
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Review berhasil ditambahkan!")
            return redirect('DetailProduct:review_page', product_id=product_id)

    context = {
        'product': product,
        'reviews': user_reviews,
        'form': form,
        'review_counts': review_counts,
        'user_has_reviewed': user_has_reviewed
    }
    return render(request, 'review_page.html', context)

@login_required(login_url='/authenticate/login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    product_id = str(review.product.id)
    if review.user != request.user:
        return redirect('DetailProduct:review_page', product_id=product_id)
        
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.last_edited = timezone.now()
            review.save()
            messages.success(request, "Review berhasil diperbarui!")
            return redirect('DetailProduct:review_page', product_id=product_id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'product_id': product_id
    }
    return render(request, 'edit_review.html', context)

@login_required(login_url='/authenticate/login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    product_id = review.product.id 
    if review.user != request.user:
        return redirect('DetailProduct:review_page', product_id=product_id)
        
    review.delete()
    messages.success(request, "Review berhasil dihapus!")
    return redirect('DetailProduct:review_page', product_id=product_id)