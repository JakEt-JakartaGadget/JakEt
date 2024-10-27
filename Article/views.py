from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel
from .forms import ArtikelForm
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

# Check if user is admin
def is_admin(user):
    return user.is_staff


def article_list(request):
    articles = Artikel.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

@user_passes_test(is_admin)
def add_article(request):
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            artikel = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Artikel berhasil ditambahkan', 'id': artikel.id}, status=200)
            return redirect('article_list')
        else:
            return JsonResponse({'message': 'Kesalahan saat menambahkan artikel', 'errors': form.errors}, status=400)
    return JsonResponse({'message': 'Metode tidak diizinkan'}, status=405)

@user_passes_test(is_admin)
def edit_article(request, pk):
    artikel = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES, instance=artikel)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Article edited successfully'}, status=200)
            return redirect('article_list')
    else:
        form = ArtikelForm(instance=artikel)
    return render(request, 'edit_article.html', {'form': form})

@user_passes_test(is_admin)
def delete_article(request, pk):
    artikel = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        artikel.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
            return JsonResponse({'message': 'Article deleted successfully'}, status=200)
        return redirect('article_list')
    return render(request, 'delete_article_confirm.html', {'artikel': artikel})


def article_detail(request, pk):
    """View to display details of a specific article."""
    artikel = get_object_or_404(Artikel, pk=pk)
    return render(request, 'article_detail.html', {'artikel': artikel})
