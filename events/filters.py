from django_filters import rest_framework as filters
from .models import Event

class EventFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    date__gte = filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    date__lte = filters.DateTimeFilter(field_name='date', lookup_expr='lte')
    organizer = filters.NumberFilter(field_name='organizer__id')

    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'date__gte', 'date__lte', 'organizer']
