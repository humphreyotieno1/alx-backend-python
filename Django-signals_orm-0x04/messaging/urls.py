from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation'),
]
