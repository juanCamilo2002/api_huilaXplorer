from django.urls import path, include
from .views import VerifyAccountCodeNumber, ResendVerificationCode, SendResetPasswordCode, ResetPassword, UserViewSet, CreateUserAdminAccountView, ActiveAccountAdminView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('auth/verify-account/', VerifyAccountCodeNumber.as_view(), name='verify_account'),
    path('auth/resend-verification-code/', ResendVerificationCode.as_view()),
    path('auth/send-reset-password-code/', SendResetPasswordCode.as_view()),
    path('auth/reset-password/', ResetPassword.as_view()),
    path('users/accounts/', include(router.urls)),
    path('users/actions/create-admin/', CreateUserAdminAccountView.as_view()),
    path('activate-account/<int:user_id>/', ActiveAccountAdminView.as_view(), name='activate_account'),
]
