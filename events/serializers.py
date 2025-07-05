from rest_framework import serializers
from .models import Event, EventRegistration
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    registrations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer', 'registrations', 'created_at', 'updated_at']

class EventRegistrationSerializer(serializers.ModelSerializer):
   event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
   user = UserSerializer(read_only=True)

   class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registered_at']

   def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
