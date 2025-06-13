from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
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
                old_content=old_message.content
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
