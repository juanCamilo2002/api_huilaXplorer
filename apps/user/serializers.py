from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.activities_turisitc_spots.models import Activities
from apps.activities_turisitc_spots.serializers import ActivitiesSerializer

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    prefrred_activities = serializers.PrimaryKeyRelatedField(
        queryset=Activities.objects.all(), many=True, required=False
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    preferred_activities = ActivitiesSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        activities_data = validated_data.pop('preferred_activities', None)
        user = User.objects.create_user(**validated_data)

        if activities_data:
            for activity_data in activities_data:
                try:
                    activity = Activities.objects.get(**activity_data)
                    user.preferred_activities.add(activity)
                except Activities.DoesNotExist:
                    raise serializers.ValidationError(
                        {"preferred_activities": f"Activity with data {activity_data} does not exist."}
                    )

        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        activities_data = validated_data.pop('preferred_activities', None)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)

        instance.save()

        if activities_data:
            instance.preferred_activities.clear()
            for activity_data in activities_data:
                try:
                    activity = Activities.objects.get(**activity_data)
                    instance.preferred_activities.add(activity)
                except Activities.DoesNotExist:
                    raise serializers.ValidationError(
                        {"preferred_activities": f"Activity with data {activity_data} does not exist."}
                    )

        return instance


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    phone_number = serializers.CharField(max_length=10)


class SendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)

class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(max_length=255)
    re_new_password = serializers.CharField(max_length=255)



class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

   