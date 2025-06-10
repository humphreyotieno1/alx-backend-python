from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Conversation, Message, ConversationParticipant

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'profile_picture')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


class ConversationParticipantInline(admin.TabularInline):
    model = ConversationParticipant
    extra = 1
    raw_id_fields = ('user',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_group', 'created_at', 'updated_at')
    list_filter = ('is_group', 'created_at', 'updated_at')
    search_fields = ('title', 'participants__email', 'participants__username')
    inlines = [ConversationParticipantInline]
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_sender', 'get_conversation', 'timestamp', 'read')
    list_filter = ('read', 'timestamp')
    search_fields = ('message_body', 'sender__email', 'sender__username', 'conversation__title')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)
    
    def get_sender(self, obj):
        return obj.sender.email if obj.sender else 'System'
    get_sender.short_description = 'Sender'
    get_sender.admin_order_field = 'sender__email'
    
    def get_conversation(self, obj):
        return obj.conversation.title or f"Conversation {obj.conversation.id}"
    get_conversation.short_description = 'Conversation'
    get_conversation.admin_order_field = 'conversation__title'
