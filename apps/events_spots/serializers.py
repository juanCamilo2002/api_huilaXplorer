from rest_framework import serializers
from .models import EventSpot


class EventSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSpot
        fields = ['id', 'name', 'description', 'date', 'tourist_spot']
