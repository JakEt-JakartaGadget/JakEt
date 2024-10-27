from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from CustomerService.models import Chat, DailyCustomerService
import json
from django.core import serializers
from django.utils import timezone
from django.db.models import OuterRef, Exists, Count, Subquery, Q 
from django.contrib.auth.models import User

@login_required
def chat_dashboard(request):
    # Only allow superusers to access the dashboard
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Get all users who have at least one chat message along with unread message counts and last chat message
    users_with_chats = User.objects.filter(
        Exists(Chat.objects.filter(user=OuterRef('pk')))
    ).annotate(
        unread_messages=Count('chat', filter=Q(chat__read=False)),
        last_chat=Subquery(
            Chat.objects.filter(user=OuterRef('pk'))
            .order_by('-date', '-time_sent')
            .values('message')[:1]
        )
    ).order_by('username')

    context = {
        'users_with_chats': users_with_chats,
    }

    return render(request, 'customerservice-dashboard.html', context)