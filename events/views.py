from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, EventRegistration
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .filters import EventFilter

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user
        if EventRegistration.objects.filter(event=event, user=user).exists():
            return Response({"detail": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)
        EventRegistration.objects.create(event=event, user=user)
       
        html_message = render_to_string('email/event_registration.html', {
            'user': user,
            'event': event,
        })
        send_mail(
            subject='Event Registration Confirmation',
            message=f'You have successfully registered for "{event.title}" on {event.date} at {event.location}.',
            from_email='tryingsomethingcool@ukr.net',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,
        )
        return Response({"detail": "Successfully registered for the event."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        event = self.get_object()
        user = request.user
        registration = EventRegistration.objects.filter(event=event, user=user)
        if not registration.exists():
            return Response({"detail": "You are not registered for this event."}, status=status.HTTP_400_BAD_REQUEST)
        registration.delete()
        return Response({"detail": "Successfully unregistered from the event."}, status=status.HTTP_200_OK)
