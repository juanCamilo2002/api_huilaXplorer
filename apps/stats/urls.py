from django.urls import path
from .views import UserAccountMonthlyStatsAPIView, TopTouristSpotsAPIView, TopActivitiesAPIView, TopRatedTouristSpotsAPIView


urlpatterns = [
    path('user-account-monthly/', UserAccountMonthlyStatsAPIView.as_view()),
    path('top-tourist-spots/', TopTouristSpotsAPIView.as_view()),
    path('top-activities/', TopActivitiesAPIView.as_view()),
     path('top-rated-tourist-spots/', TopRatedTouristSpotsAPIView.as_view()),
]