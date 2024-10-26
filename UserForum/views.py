from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Discussion, Reply
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def forum_view(request):
    discussions = Discussion.objects.all().order_by('-started')
    context = {
        'discussions': discussions,
        'is_superuser': request.user.is_superuser  # Add this line
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
