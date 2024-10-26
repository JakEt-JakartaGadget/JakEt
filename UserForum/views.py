from datetime import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Discussion, Reply
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def forum_view(request):
    discussions = Discussion.objects.all().order_by('-started')
    context = {
        'discussions': discussions,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'user-forum.html', context)

@login_required
def add_discussion(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        if topic:
            new_discussion = Discussion.objects.create(
                owner=request.user,
                topic=topic
            )
            return JsonResponse({
                'success': True, 
                'topic': topic,
                'id': str(new_discussion.id),
                'username': request.user.username,
                'profile_picture': request.user.profile_picture.url if hasattr(request.user, 'profile_picture') else '',
                'created_at': new_discussion.started.strftime("%Y-%m-%d %H:%M:%S")
            })
    return JsonResponse({'success': False})

@user_passes_test(lambda u: u.is_superuser)
def delete_discussion(request, discussion_id):
    try:
        discussion = Discussion.objects.get(id=discussion_id)
        discussion.delete()
        return JsonResponse({'success': True})
    except Discussion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Discussion not found'}, status=404)
    

@login_required
def discussion_view(request, id):
    discussion = Discussion.objects.get(id=id)
    replies =  Reply.objects.filter(discussion=discussion).order_by('-replied')
    context = {
        'discussion': discussion,
        'replies': replies,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'discussion.html', context)

@login_required
@csrf_exempt
def send_reply(request, id):
    try:
        discussion = Discussion.objects.get(id=id)
    except Discussion.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Discussion not found'}, status=404)

    # Parse the JSON data from the request
    data = json.loads(request.body)
    message = data.get('message', '').strip()

    # Check if the message is empty
    if not message:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    # If the discussion exists and the message is valid, save the reply
    reply = Reply.objects.create(discussion=discussion, sender=request.user, message=message)
    return JsonResponse({
        'status': 'success',
        'message': {
            'message': reply.message,
            'sender': {'username': reply.sender.username}
        }
    })

    new_reply = Reply.objects.latest('created_at')
    return JsonResponse({'message': {
        'message': new_reply.message,
        'sender': {'username': new_reply.sender.username, 'profile_picture': new_reply.sender.profile_picture.url}
    }})