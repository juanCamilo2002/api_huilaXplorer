from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivitiesViewSet

router = DefaultRouter()

router.register('activities-spots', ActivitiesViewSet)


urlpatterns = [
    path('', include(router.urls))
]