from django.shortcuts import render, get_object_or_404
from .models import Artikel

def artikel_list(request):
    artikels = Artikel.objects.all().order_by('-published_date')
    return render(request, 'artikel_list.html', {'artikels': artikels})

def artikel_detail(request, pk):
    artikel = get_object_or_404(Artikel, pk=pk)
    return render(request, 'artikel_detail.html', {'artikel': artikel})
