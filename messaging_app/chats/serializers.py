from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'profile_picture', 'online')
        read_only_fields = ('user_id',)


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ('message_id', 'sender', 'sender_name', 'text', 'message_body', 
                  'sent_at', 'timestamp', 'read')
        read_only_fields = ('message_id', 'sent_at', 'timestamp')
    
    def get_sender_name(self, obj):
        return obj.sender.username


class ConversationListSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants', 'created_at', 'updated_at', 'last_message')
        read_only_fields = ('conversation_id', 'created_at', 'updated_at')
    
    def get_last_message(self, obj):
        message = obj.messages.order_by('-sent_at').first()
        if message:
            return MessageSerializer(message).data
        return None


class ConversationDetailSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants', 'created_at', 'updated_at', 'messages')
        read_only_fields = ('conversation_id', 'created_at', 'updated_at')


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants')
        read_only_fields = ('conversation_id',)