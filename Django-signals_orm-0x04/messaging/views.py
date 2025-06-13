from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_view(request, user_id):
    """
    View that displays messages in a conversation between two users
    """
    # Get the other user in the conversation
    other_user = get_object_or_404(User, id=user_id)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # Mark messages as read if they were sent to the current user
    unread_messages = messages.filter(receiver=request.user, read=False)
    unread_messages.update(read=True)
    
    context = {
        'messages': messages,
        'other_user': other_user
    }
    
    return render(request, 'conversation.html', context)
