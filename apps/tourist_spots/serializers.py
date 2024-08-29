from rest_framework import serializers
from .models import TouristSpot, TouristSpotsImage, LocationSpot
from apps.activities_turisitc_spots.serializers import ActivitiesSerializer
from apps.activities_turisitc_spots.models import Activities

class LocationSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationSpot
        fields = ['id', 'name']

class TouristSpotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristSpotsImage
        fields = ['id', 'image', 'caption', 'tourist_spot']


class TouristSpotSerializer(serializers.ModelSerializer):
    images = TouristSpotImageSerializer(many=True, read_only=True)
    activities = ActivitiesSerializer(many=True)
    location = LocationSpotSerializer()
    
    class Meta:
        model = TouristSpot
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'images', 'location', 'activities']

    
    def create(self, validated_data):
        activities_data = validated_data.pop('activities')
        location_data= validated_data.pop('location')

        try:
            location = LocationSpot.objects.get(**location_data)
        except LocationSpot.DoesNotExist:
            raise serializers.ValidationError(
                {"location": f"Location with data {location_data} does not exist."}
                )

        spot = TouristSpot.objects.create(location=location, **validated_data)

        for activity_data in activities_data:
            try:
                activity = Activities.objects.get(**activity_data)
                spot.activities.add(activity)
            except Activities.DoesNotExist:
                raise serializers.ValidationError(
                    {"activities": f"Activity with data {activity_data} does not exist."}
                    )
        return spot
    
    def update(self, instance, validated_data):
        activities_data = validated_data.pop('activities', None)
        location_data = validated_data.pop('location', None)

        if location_data:
            try:
                location = LocationSpot.objects.get(**location_data)
            except LocationSpot.DoesNotExist:
                raise serializers.ValidationError(
                    {"location": f"Location with data {location_data} does not exist."}
                    )
            instance.location = location


        if activities_data is not None:
            instance.activities.clear()
            for activity_data in activities_data:
                try:
                    activity = Activities.objects.get(**activity_data)
                    instance.activities.add(activity)
                except Activities.DoesNotExist:
                    raise serializers.ValidationError(
                        {"activities": f"Activity with data {activity_data} does not exist."}
                        )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance