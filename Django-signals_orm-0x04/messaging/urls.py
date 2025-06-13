from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation'),
    path('message/<int:message_id>/history/', views.message_history_view, name='message_history'),
    path('delete-account/', views.delete_user, name='delete_user'),
]
