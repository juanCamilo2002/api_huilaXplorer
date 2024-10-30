from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.activities_turisitc_spots.models import Activities
from apps.activities_turisitc_spots.serializers import ActivitiesSerializer
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    prefrred_activities = serializers.PrimaryKeyRelatedField(
        queryset=Activities.objects.all(), many=True, required=False
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # No requerido
        }

class UserSerializer(serializers.ModelSerializer):
    preferred_activities = ActivitiesSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # No requerido
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



    
    


class UserCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'is_staff']

    password = serializers.CharField(write_only=True)  
    is_staff = serializers.BooleanField(default=False)  

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'is_staff']

    def create(self, validated_data):
        # Extraer la contraseña y el estado de admin
        password = validated_data.pop('password')
        is_staff = validated_data.pop('is_staff', False)

        # Crear un usuario administrador o normal
        if is_staff:
            user = User.objects.create_superuser(password=password, **validated_data)
        else:
            user = User.objects.create_user(password=password, **validated_data)

        # Enviar el correo de activación
        self.send_activation_email(user)

        return user

    def send_activation_email(self, user):
        # Genera el link de activación
        activation_link = reverse(
            'activate_account', kwargs={'user_id': user.id})
        full_activation_link = f"{settings.FRONTEND_URL}{activation_link}"

        # Envía el correo
        send_mail(
            subject='Activate your account',
            message=f'Click the link to activate your account: {full_activation_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )


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
