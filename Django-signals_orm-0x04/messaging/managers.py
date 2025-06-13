from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Returns all unread messages for the given user
        """
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender')
