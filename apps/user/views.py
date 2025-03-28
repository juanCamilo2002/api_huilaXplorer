from rest_framework.views import APIView
from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from .utils import send_verification_code, send_reset_pass_code
from django.utils import timezone
from .serializers import UserSerializer, VerifyCodeSerializer, SendCodeSerializer, ResetPasswordSerializer, ErrorResponseSerializer, SuccessResponseSerializer, UserCreateAdminSerializer
from .custom_permissions import IsAdminOrIsSelf
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            # Verifica si la cuenta no está activa
            user = User.objects.filter(email=request.data.get("email")).first()
            if user and not user.is_active:
                return Response(
                    {"error": "Cuenta inactiva."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Si no es un problema de cuenta inactiva, asumimos que son credenciales inválidas
            return Response(
                {"error": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

class VerifyAccountCodeNumber(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary='Verify account code number',
        description="This endpoint is used to verify the account code number",
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer
        },
        request=VerifyCodeSerializer
    )
    def post(self, request, format=None, *args, **kwargs):
        """
        This endpoint is used to verify the account code number
        """
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

    @extend_schema(
        summary='Resend verification code',
        description="This endpoint is used to resend the verification code",
        responses={
            200: SuccessResponseSerializer,
            404: ErrorResponseSerializer
        },
        request=SendCodeSerializer
    )
    def post(self, request, format=None, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        try:
            user = User.objects.get(phone_number=phone_number)

            # generate a new code
            sender_code = send_reset_pass_code(user)

            if sender_code["messages"][0]["status"] != "0":
                return Response({'error': 'Error sending code'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# vista para enviar codigo para reestablecer contraseña

class SendResetPasswordCode(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary='Send reset password code',
        description="This endpoint is used to send the reset password code",
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer},
        request=SendCodeSerializer
    )
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

class VerifyResetPasswordCode(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        try:
            user = User.objects.get(phone_number=phone_number)

            datetime_now = timezone.now()

            if datetime_now > user.expiration_code_reset_password:
                return Response({'error': 'Code expired'}, status=status.HTTP_410_GONE)

            if user.code_reset_password != code:
                return Response({'error': 'Invalid code'}, status=status.HTTP_403_FORBIDDEN)


            return Response({'message': 'Code verified successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# reestablecer contraseña
class ResetPassword(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary='Reset password',
        description="This endpoint is used to reset the password of an account",
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer
        },
        request=ResetPasswordSerializer
    )
    def post(self, request, format=None, *args, **kwargs):

        phone_number = request.data.get('phone_number')
        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')

        try:
            user = User.objects.get(phone_number=phone_number)
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone_number', 'email']

    def get_permissions(self):
        actions = ['retrieve', 'update', 'partial_update', 'destroy']
        if self.action in actions:
            permission_classes = [IsAdminOrIsSelf]
        elif self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
    

class CreateUserAdminAccountView(generics.CreateAPIView):
    serializer_class = UserCreateAdminSerializer
    permission_classes = [permissions.IsAdminUser]

class ActiveAccountAdminView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    


