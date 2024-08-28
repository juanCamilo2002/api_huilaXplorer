from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TouristSpotViewSet, TouristSpotImageViewSet

router = DefaultRouter()
router.register('tourist-spots', TouristSpotViewSet)
router.register('tourist-spot-images', TouristSpotImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
