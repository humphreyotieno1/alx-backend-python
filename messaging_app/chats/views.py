from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import (
    ConversationCreateSerializer,
    MessageSerializer,
    UserSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conversation_id', 'created_at']
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_queryset(self):
        # Filter conversations to only show those the user is participating in
        return Conversation.objects.filter(participants=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Add a message to this conversation"""
        conversation = self.get_object()
        
        # Check if user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create message data with the sender set to current user
        message_data = request.data.copy()
        message_data['sender'] = request.user.user_id
        message_data['conversation'] = conversation.conversation_id
        
        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing messages
    """
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['message_id', 'sender', 'created_at']
    search_fields = ['content']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        # Get the conversation ID from the URL parameter
        conversation_id = self.request.query_params.get('conversation', None)
        
        if conversation_id:
            # Check if user is a participant in the conversation
            conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
            if self.request.user in conversation.participants.all():
                return Message.objects.filter(conversation=conversation)
            return Message.objects.none()
        
        # Return messages from all conversations where the user is a participant
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations)
