from django.urls import path
from .views import UserTouristRoutesAPIView, CreateTouristRouteAPIView, UpdateTouristRouteAPIView, DeleteTouristRouteAPIView, TouristRouteDetailAPIView, GenerateRouteActivitiesView


urlpatterns = [
    path('me', UserTouristRoutesAPIView.as_view()),
    path('create', CreateTouristRouteAPIView.as_view()),
    path('update/<int:pk>', UpdateTouristRouteAPIView.as_view()),
    path('delete/<int:pk>', DeleteTouristRouteAPIView.as_view()),
    path('<int:pk>', TouristRouteDetailAPIView.as_view()),
    path('<int:route_id>/activities', GenerateRouteActivitiesView.as_view(), name='generate_activities'),

]
