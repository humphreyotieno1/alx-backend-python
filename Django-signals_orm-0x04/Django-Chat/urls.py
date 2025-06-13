from django.urls import path
from . import views

app_name = 'django_chat'

urlpatterns = [
    path('delete-account/', views.delete_user, name='delete_user'),
]
