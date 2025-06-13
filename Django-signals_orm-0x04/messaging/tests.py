from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='testpass123')
        self.receiver = User.objects.create_user(username='receiver', password='testpass123')

    def test_message_creation_creates_notification(self):
        """
        Test that creating a message automatically creates a notification for the receiver
        """
        # Start with no notifications
        self.assertEqual(Notification.objects.count(), 0)

        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )

        # Check that notification was created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
