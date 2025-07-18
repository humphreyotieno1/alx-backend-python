from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Conversation, Message, User
from .serializers import ConversationCreateSerializer, MessageSerializer, UserSerializer
from .permissions import IsMessageOwner, IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return []  # No authentication required for user registration
        return [permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationCreateSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'participants__username']
    ordering_fields = ['created_at', 'updated_at']
    filterset_fields = ['participants']
    
    def get_queryset(self):
        # Users can only see conversations they are part of
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically add the current user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'User ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response(
                {'status': 'User added to conversation'}, 
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['content']
    ordering_fields = ['timestamp', 'is_read']
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    
    def get_queryset(self):
        """
        Return messages where the current user is a participant of the conversation.
        """
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')
    
    def filter_queryset(self, queryset):
        """
        Apply all the filters to the queryset.
        """
        queryset = super().filter_queryset(queryset)
        
        # Apply additional filtering for the current user
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        
        return queryset.distinct()
    
    def get_queryset(self):
        # Only show messages from conversations the user is a participant of
        return Message.objects.filter(conversation__participants=self.request.user)
    
    def perform_create(self, serializer):
        # Get the conversation from the request data
        conversation = serializer.validated_data.get('conversation')
        
        # Check if the user is a participant of the conversation
        if conversation and self.request.user not in conversation.participants.all():
            raise PermissionDenied({"detail": "You are not a participant of this conversation."})
        
        # Automatically set the sender to the current user
        serializer.save(sender=self.request.user)
        
        # Update the conversation's updated_at timestamp
        conversation.save()
    
    def update(self, request, *args, **kwargs):
        # Get the message object
        message = self.get_object()
        
        # Check if the user is the sender of the message
        if message.sender != request.user:
            return Response(
                {"detail": "You can only update your own messages."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Check if the user is a participant of the conversation
        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Get the message object
        message = self.get_object()
        conversation_id = message.conversation.id
        
        # Check if the user is the sender of the message
        if message.sender != request.user:
            return Response(
                {"detail": "You can only delete your own messages."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Check if the user is a participant of the conversation
        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        response = super().destroy(request, *args, **kwargs)
        
        # Update the conversation's updated_at timestamp after message deletion
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            conversation.save()
        except Conversation.DoesNotExist:
            pass
            
        return response
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Ensure the sender is the current user
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
