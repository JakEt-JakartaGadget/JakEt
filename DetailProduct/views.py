from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from Homepage.models import Phone
from .models import Review
import json
from django.db.models import Avg

@login_required(login_url='/authenticate/login')
def product_detail(request, product_id):
    product = get_object_or_404(Phone, id=product_id)
    reviews = Review.objects.filter(product=product)
    
    user_has_review = reviews.filter(user=request.user).exists() if request.user.is_authenticated else False
    user_review = reviews.filter(user=request.user).first() if user_has_review else None

    context = {
        'product': product,
        'reviews': reviews,
        'user_has_review': user_has_review,
        'user_review': user_review,
    }
    return render(request, 'detail.html', context)


@login_required
@require_POST
def submit_review(request, product_id):
    try:
        data = json.loads(request.body)
        content = data.get('content')
        rating = data.get('rating', 5)
        product = get_object_or_404(Phone, id=product_id)
        
        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={
                'content': content,
                'rating': rating
            }
        )
        
        avg_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        product.rating = round(avg_rating) if avg_rating else 0
        product.save()
        
        return JsonResponse({
            'success': True,
            'review': {
                'user': review.user.username,
                'content': review.content,
                'rating': review.rating,
                'date_added': review.date_added.strftime('%Y-%m-%d %H:%M')
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@login_required
def toggle_favorite(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Phone, id=product_id)
        if hasattr(request.user, 'userdata'):
            is_favorite = request.user.userdata.favorite_phones.filter(id=product.id).exists()
            if is_favorite:
                request.user.userdata.favorite_phones.remove(product)
                is_favorite = False
            else:
                request.user.userdata.favorite_phones.add(product)
                is_favorite = True
            return JsonResponse({'success': True, 'is_favorite': is_favorite})
    return JsonResponse({'success': False}, status=400)

@login_required
@csrf_exempt
def rate_product(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating = int(data.get('rating'))
            product = get_object_or_404(Phone, id=product_id)
            
            review, created = Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'rating': rating}
            )
            
            avg_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
            product.rating = round(avg_rating) if avg_rating else 0
            product.save()
            
            return JsonResponse({'success': True, 'new_rating': product.rating})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False}, status=400)

@login_required
def edit_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id, user=request.user)
        data = json.loads(request.body)
        
        review.content = data['content']
        review.rating = data['rating']
        review.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
