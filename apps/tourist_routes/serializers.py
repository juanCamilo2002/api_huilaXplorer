from rest_framework import serializers
from .models import TouristRoute, ActivityRoute
from apps.tourist_spots.serializers import TouristSpotSerializer
from apps.user.serializers import UserSerializer


class ActivityRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRoute
        fields = ['id', 'date', 'tourist_spot']

class TouristRouteSerializer(serializers.ModelSerializer):
    activity_routes = ActivityRouteSerializer(many=True)

    class Meta:
        model = TouristRoute
        fields =  ['id','name', 'description', 'date_start', 'date_end', 'activity_routes']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        activities_data = validated_data.pop('activity_routes', [])

        # asign the user to the tourist route
        tourist_route = TouristRoute.objects.create(user=self.context['request'].user, **validated_data)

        # create the activities
        for activity in activities_data:
            ActivityRoute.objects.create(route=tourist_route, **activity)

        return tourist_route
    
    def update(self, instance, validated_data):
        # update the ToristRoute fields
        activities_data = validated_data.pop('activity_routes', [])

        # Update the main fileds of the TouristRoute instance
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_end = validated_data.get('date_start', instance.date_end)
        instance.save()

        # Manage the activities related to the route
        existing_activities = {activity.id: activity for activity in instance.activity_routes.all()}
        new_activities = []

        for activity in activities_data:
            # If the activity already exists, update it
            activity_id = activity.get('id', None)
            if activity_id and activity_id in existing_activities:
                existing_activity = existing_activities.pop(activity_id)
                existing_activity.date = activity.get('date', existing_activity.date)
                existing_activity.tourist_spot = activity.get('tourist_spot', existing_activity.tourist_spot)
                existing_activity.save()
            else:
                # Otherwise, add a new activity
                new_activities.append(ActivityRoute(route=instance, **activity))
        
        # Delete remaining activities not sent in the request
        for activity in existing_activities.values():
            activity.delete()

        
        # Bulk create new activities
        ActivityRoute.objects.bulk_create(new_activities)

        return instance
