from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventSpotViewSet

router = DefaultRouter()

router.register('event-spots', EventSpotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
