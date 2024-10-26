# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel
from .forms import ArtikelForm
from django.contrib.auth.decorators import user_passes_test

# Check if user is admin
def is_admin(user):
    return user.is_staff


def article_list(request):
    """View to list all articles."""
    articles = Artikel.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

@user_passes_test(is_admin)
def add_article(request):
    """View to add a new article."""
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArtikelForm()
    return render(request, 'add_article.html', {'form': form})

@user_passes_test(is_admin)
def edit_article(request, pk):
    """View to edit an existing article."""
    artikel = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES, instance=artikel)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArtikelForm(instance=artikel)
    return render(request, 'edit_article.html', {'form': form})

@user_passes_test(is_admin)
def delete_article(request, pk):
    """View to delete an article."""
    artikel = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        artikel.delete()
        return redirect('article_list')
    return render(request, 'delete_article_confirm.html', {'artikel': artikel})


def article_detail(request, pk):
    """View to display details of a specific article."""
    artikel = get_object_or_404(Artikel, pk=pk)
    return render(request, 'article_detail.html', {'artikel': artikel})
