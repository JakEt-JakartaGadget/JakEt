# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Chat, DailyCustomerService
import json
from django.core import serializers
from django.utils import timezone

@login_required
def customer_service(request):
    # Get or create today's customer service instance
    daily_service, created = DailyCustomerService.objects.get_or_create(
        user=request.user,
        date=timezone.now().date()
    )
    
    # Get recent messages
    messages = Chat.objects.filter(
        user=request.user
    ).order_by('date', 'time_sent')[:50]  # Limit to last 50 messages
    
    context = {
        'messages': messages
    }
    return render(request, 'customer-service.html', context)

@login_required
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            
            if message:
                chat = Chat.objects.create(
                    user=request.user,
                    message=message
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'id': chat.id,
                        'message': chat.message,
                        'time': chat.time_sent.strftime('%H:%M'),
                        'date': chat.date.strftime('%Y-%m-%d')
                    }
                })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def get_messages(request):
    # Get messages after a certain timestamp
    last_msg_time = request.GET.get('after', None)
    
    messages = Chat.objects.filter(
        user=request.user
    )
    
    if last_msg_time:
        messages = messages.filter(time_sent__gt=last_msg_time)
    
    messages = messages.order_by('date', 'time_sent')
    
    data = [{
        'id': msg.id,
        'message': msg.message,
        'time': msg.time_sent.strftime('%H:%M'),
        'date': msg.date.strftime('%Y-%m-%d')
    } for msg in messages]
    
    return JsonResponse({'messages': data})