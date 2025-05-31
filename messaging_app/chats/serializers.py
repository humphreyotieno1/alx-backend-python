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
    # Add a CharField with validation
    text = serializers.CharField(max_length=500, required=True)
    
    class Meta:
        model = Message
        fields = ('message_id', 'sender', 'sender_name', 'text', 'message_body', 
                  'sent_at', 'timestamp', 'read')
        read_only_fields = ('message_id', 'sent_at', 'timestamp')
    
    def get_sender_name(self, obj):
        return obj.sender.username
    
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message text cannot be empty.")
        return value


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants')
        read_only_fields = ('conversation_id',)
    
    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Conversation must have at least 2 participants.")
        return value
