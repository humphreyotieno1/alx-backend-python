from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an 'owner' attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named 'owner'.
        return obj.owner == request.user

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to view it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        return request.user in obj.participants.all()

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    - Allow only authenticated users
    - Allow only participants to access the conversation and its messages
    """
    def has_permission(self, request, view):
        # Only allow authenticated users
        if not request.user or not request.user.is_authenticated:
            return False
            
        # For list and create actions, we'll check in the view
        if view.action in ['list', 'create']:
            return True
            
        # For other actions, we'll check object-level permissions
        return True
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        is_participant = request.user in obj.participants.all()
        
        # For GET, HEAD, OPTIONS (safe methods)
        if request.method in SAFE_METHODS:
            return is_participant
            
        # For PUT, PATCH, DELETE - only allow if user is participant
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant
            
        # Default deny
        return False

class IsMessageOwner(BasePermission):
    """
    Custom permission to only allow the sender of a message to modify it.
    """
    def has_permission(self, request, view):
        # Only allow authenticated users
        if not request.user or not request.user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for participants
        if request.method in SAFE_METHODS:
            return request.user in obj.conversation.participants.all()
            
        # Check if the user is the sender of the message
        return obj.sender == request.user
