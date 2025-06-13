from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Log the old content of a message before it's updated
    """
    if instance.pk:  # Check if this is an update (not a new message)
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:  # Only log if content changed
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content,
                edited_by=instance.sender
            )
            instance.edited = True

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Create a notification for the receiver when a new message is created
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Clean up all user-related data when a user is deleted
    """
    # Delete all messages sent by the user
    Message.objects.filter(sender=instance).delete()
    
    # Delete all messages received by the user
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications related to the user
    Notification.objects.filter(user=instance).delete()
    
    # Delete all message histories related to the user
    # This will be handled by CASCADE due to ForeignKey constraints
    # but we're being explicit here for clarity
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
