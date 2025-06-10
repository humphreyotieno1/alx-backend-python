from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationCreateSerializer, MessageSerializer, UserSerializer
from .permissions import IsParticipant, IsMessageOwner, IsOwnerOrReadOnly, IsParticipantOfConversation

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
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['content']
    ordering_fields = ['timestamp']
    filterset_fields = ['conversation', 'sender', 'is_read']
    
    def get_queryset(self):
        # Only show messages from conversations the user is a participant of
        return Message.objects.filter(conversation__participants=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the sender to the current user
        serializer.save(sender=self.request.user)
        
        # Update the conversation's updated_at timestamp
        conversation = serializer.validated_data['conversation']
        conversation.save()
    
    def get_queryset(self):
        # Users can only see messages from conversations they are part of
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')
    
    def perform_create(self, serializer):
        # Automatically set the sender to the current user
        serializer.save(sender=self.request.user)
    
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
