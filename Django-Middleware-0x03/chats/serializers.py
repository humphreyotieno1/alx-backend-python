from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Conversation, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone_number', 'profile_picture'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        # Remove password2 from the data
        validated_data.pop('password2', None)
        
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
        )
        
        # Set the password
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    text = serializers.CharField(max_length=500, required=True, write_only=True)
    
    class Meta:
        model = Message
        fields = (
            'id', 'conversation', 'sender', 'sender_name', 
            'text', 'message_body', 'timestamp', 'read'
        )
        read_only_fields = ('id', 'timestamp', 'sender_name')
    
    def get_sender_name(self, obj):
        return obj.sender.username if obj.sender else None
    
    def validate(self, data):
        # Ensure the conversation exists and the user is a participant
        conversation = data.get('conversation')
        request = self.context.get('request')
        
        if conversation and request and request.user:
            if not conversation.participants.filter(id=request.user.id).exists():
                raise serializers.ValidationError(
                    "You are not a participant of this conversation."
                )
        
        # Copy text to message_body for backward compatibility
        if 'text' in data:
            data['message_body'] = data['text']
        
        return data
    
    def create(self, validated_data):
        # Ensure the sender is set to the current user
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all(),
        required=True
    )
    title = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'participants', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_participants(self, value):
        # Ensure there are at least 2 unique participants
        if len(value) < 1:
            raise serializers.ValidationError("Conversation must have at least 1 other participant.")
        
        # Ensure all participants exist
        user_ids = [user.id for user in value]
        if len(user_ids) != User.objects.filter(id__in=user_ids).count():
            raise serializers.ValidationError("One or more participants do not exist.")
            
        return value
    
    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants
        for participant in participants:
            conversation.participants.add(participant)
        
        # Add the current user if not already in participants
        request = self.context.get('request')
        if request and request.user not in participants:
            conversation.participants.add(request.user)
        
        # Set a default title if not provided
        if not conversation.title:
            usernames = [user.username for user in conversation.participants.all()]
            conversation.title = ', '.join(usernames[:3])
            if len(usernames) > 3:
                conversation.title += f" and {len(usernames) - 3} more"
            conversation.save()
        
        return conversation
