from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel
from .forms import ArtikelForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse, HttpResponse
from django.core import serializers


def is_admin(user):
    """Check if the user is an admin."""
    return user.is_staff


@login_required
def get_user_role(request):
    """
    API endpoint to get the role of the logged-in user.
    Returns a JSON response with the role information.
    """
    role = "admin" if request.user.is_staff else "user"
    return JsonResponse({'role': role}, status=200)


def article_list(request):
    """View to list all articles."""
    articles = Artikel.objects.all()
    return render(request, 'article_list.html', {'articles': articles})


@user_passes_test(is_admin)
def add_article(request):
    """View to add a new article."""
    if request.method == 'POST':
        form = ArtikelForm(request.POST)
        if form.is_valid():
            artikel = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX
                return JsonResponse({'message': 'Article added successfully', 'id': artikel.id}, status=201)
            return redirect('article_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX errors
                return JsonResponse({'message': 'Error while adding the article', 'errors': form.errors}, status=400)
            return HttpResponse("Invalid form submission", status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@user_passes_test(is_admin)
def edit_article(request, pk):
    """View to edit an existing article."""
    artikel = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        form = ArtikelForm(request.POST, instance=artikel)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX
                return JsonResponse({'message': 'Article edited successfully'}, status=200)
            return redirect('article_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX errors
                return JsonResponse({'message': 'Error while editing the article', 'errors': form.errors}, status=400)
            return HttpResponse("Invalid form submission", status=400)
    else:
        form = ArtikelForm(instance=artikel)
    return render(request, 'edit_article.html', {'form': form, 'artikel': artikel})


@user_passes_test(is_admin)
def delete_article(request, pk):
    """View to delete an article."""
    artikel = get_object_or_404(Artikel, pk=pk)
    if request.method == 'POST':
        artikel.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX
            return JsonResponse({'message': 'Article deleted successfully'}, status=200)
        return redirect('article_list')
    return render(request, 'delete_article_confirm.html', {'artikel': artikel})


def article_detail(request, pk):
    """View to display details of a specific article."""
    artikel = get_object_or_404(Artikel, pk=pk)
    return render(request, 'article_detail.html', {'artikel': artikel})


def show_json(request):
    """View to return all articles in JSON format."""
    data = Artikel.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml(request):
    """View to return all articles in XML format."""
    data = Artikel.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
