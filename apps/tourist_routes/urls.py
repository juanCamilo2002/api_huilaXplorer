from django.urls import path
from .views import UserTouristRoutesAPIView, CreateTouristRouteAPIView, UpdateTouristRouteAPIView, DeleteTouristRouteAPIView


urlpatterns = [
    path('me', UserTouristRoutesAPIView.as_view()),
    path('create', CreateTouristRouteAPIView.as_view()),
    path('update/<int:pk>', UpdateTouristRouteAPIView.as_view()),
    path('delete/<int:pk>', DeleteTouristRouteAPIView.as_view()),
]
