import django_filters
from django.db import models
from .models import Message
from django.utils import timezone
from datetime import timedelta

class MessageFilter(django_filters.FilterSet):
    """
    Filter for messages with support for:
    - Filtering by conversation ID
    - Filtering by sender ID
    - Filtering by read status
    - Date range filtering
    - Search in message content
    """
    conversation = django_filters.NumberFilter(
        field_name='conversation__id',
        lookup_expr='exact',
        label='Filter by conversation ID'
    )
    
    sender = django_filters.NumberFilter(
        field_name='sender__id',
        lookup_expr='exact',
        label='Filter by sender ID'
    )
    
    is_read = django_filters.BooleanFilter(
        field_name='is_read',
        lookup_expr='exact',
        label='Filter by read status'
    )
    
    date_after = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte',
        label='Messages after this date',
        method='filter_date_after'
    )
    
    date_before = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte',
        label='Messages before this date',
        method='filter_date_before'
    )
    
    last_n_days = django_filters.NumberFilter(
        method='filter_last_n_days',
        label='Messages from the last N days'
    )
    
    search = django_filters.CharFilter(
        field_name='content',
        lookup_expr='icontains',
        label='Search in message content'
    )
    
    class Meta:
        model = Message
        fields = {
            'timestamp': ['lt', 'gt', 'lte', 'gte'],
        }
    
    def filter_date_after(self, queryset, name, value):
        return queryset.filter(timestamp__gte=value)
    
    def filter_date_before(self, queryset, name, value):
        return queryset.filter(timestamp__lte=value)
    
    def filter_last_n_days(self, queryset, name, value):
        try:
            days = int(value)
            date_n_days_ago = timezone.now() - timedelta(days=days)
            return queryset.filter(timestamp__gte=date_n_days_ago)
        except (ValueError, TypeError):
            return queryset.none()
    
    def filter_queryset(self, queryset):
        # Ensure we're only showing messages from conversations the user is part of
        queryset = queryset.filter(conversation__participants=self.request.user)
        return super().filter_queryset(queryset)
