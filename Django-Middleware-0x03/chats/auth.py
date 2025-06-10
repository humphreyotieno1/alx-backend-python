"""
Custom authentication classes and utilities for the chats app.
"""
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenAuthentication(authentication.TokenAuthentication):
    """
    Custom token authentication that uses the user's email as the token.
    This is just an example - you can modify it to fit your needs.
    """
    keyword = 'Token'
    
    def authenticate_credentials(self, key):
        try:
            user = User.objects.get(email=key)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
            
        return (user, None)

# You can add more custom authentication classes or utilities below
