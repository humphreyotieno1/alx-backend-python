from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message, MessageHistory

@login_required
def delete_user(request):
    """
    View to allow users to delete their account
    """
    if request.method == 'POST':
        # Delete the user
        request.user.delete()
        # Log out the user
        logout(request)
        # Show success message
        messages.success(request, 'Your account has been successfully deleted.')
        # Redirect to login page
        return redirect('login')
    return render(request, 'delete_user.html')

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_view(request, user_id):
    """
    View that displays messages in a conversation between two users
    """
    # Get the other user in the conversation
    other_user = get_object_or_404(User, id=user_id)
    
    # Get all messages between the two users with optimized queries
    messages = (
    Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver', 'parent_message')
    .prefetch_related('history')
    .only('id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'read', 'parent_message')
    .order_by('timestamp')
)
    
    # Mark messages as read if they were sent to the current user
    unread_messages = messages.filter(receiver=request.user, read=False)
    unread_messages.update(read=True)
    
    # Get unread messages for the user
    unread_messages = Message.unread.unread_for_user(request.user).only(
    'id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'read')
    
    context = {
        'messages': messages,
        'other_user': other_user,
        'unread_messages': unread_messages
    }
    
    return render(request, 'conversation.html', context)

@login_required
def message_history_view(request, message_id):
    """
    View to display message edit history
    """
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
    
    context = {
        'message': message,
        'history': history
    }
    
    return render(request, 'message_history.html', context)
