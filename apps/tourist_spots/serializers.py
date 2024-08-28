from rest_framework import serializers
from .models import TouristSpot, TouristSpotsImage

class TouristSpotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristSpotsImage
        fields = ['id', 'image', 'caption', 'tourist_spot']


class TouristSpotSerializer(serializers.ModelSerializer):
    images = TouristSpotImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = TouristSpot
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'images', 'location']