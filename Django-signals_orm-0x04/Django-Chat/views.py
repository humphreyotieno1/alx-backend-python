from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def delete_user(request):
    """
    View to allow users to delete their account
    """
    if request.method == 'POST':
        # Get the current user
        user = request.user
        
        # Delete the user
        user.delete()
        
        # Log out the user
        logout(request)
        
        # Show success message
        messages.success(request, 'Your account has been successfully deleted.')
        
        # Redirect to login page
        return redirect('login')
    
    return render(request, 'delete_user.html')
