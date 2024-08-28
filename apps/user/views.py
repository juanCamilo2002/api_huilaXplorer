from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .utils import send_verification_code, send_reset_pass_code
from django.utils import timezone
from .serializers import UserSerializer
from .custom_permissions import IsAdminOrIsSelf

User = get_user_model()


class VerifyAccountCodeNumber(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        try:
            user = User.objects.get(phone_number=phone_number)

            if user.verification_code != code:
                return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.verification_code = None
            user.save()

            return Response({'message': 'Account verified succesfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ResendVerificationCode(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        try:
            user = User.objects.get(phone_number=phone_number)

            # generate a new code
            send_verification_code(user)
            return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# vista para enviar codigo para reestablecer contraseña

class SendResetPasswordCode(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        try:
            user = User.objects.get(phone_number=phone_number)

            # send code
            sender_code = send_reset_pass_code(user)

            if sender_code["messages"][0]["status"] != "0":
                return Response({'error': 'Error sending code'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Code sent successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': "User not found"}, status=status.HTTP_404_NOT_FOUND)


# reestablecer contraseña
class ResetPassword(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):

        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')

        try:
            user = User.objects.get(phone_number=phone_number)

            datetime_now = timezone.now()

            if datetime_now > user.expiration_code_reset_password:
                return Response({'error': 'Code expired'}, status=status.HTTP_400_BAD_REQUEST)

            if user.code_reset_password != code:
                return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != re_new_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.code_reset_password = None
            user.expiration_code_reset_password = None
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        actions = ['retrieve', 'update', 'partial_update', 'destroy']
        if self.action == actions:
            permission_classes = [IsAdminOrIsSelf]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
