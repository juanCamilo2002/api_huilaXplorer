from rest_framework import viewsets
from .models import TouristSpot, TouristSpotsImage, LocationSpot
from rest_framework import permissions
from .serializers import TouristSpotImageSerializer, TouristSpotSerializer, LocationSpotSerializer

class LocationSoptViewSet(viewsets.ModelViewSet):
    queryset = LocationSpot.objects.all()
    serializer_class = LocationSpotSerializer

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy', 'create']
        if self.action in actions:
            permissions_classes = [permissions.IsAdminUser]
        else:
            permissions_classes = [permissions.AllowAny]

        return [permission() for permission in permissions_classes]


class TouristSpotViewSet(viewsets.ModelViewSet):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy', 'create']
        if self.action in actions:
            permissions_classes = [permissions.IsAdminUser]
        else:
            permissions_classes = [permissions.AllowAny]

        return [permission() for permission in permissions_classes]


class TouristSpotImageViewSet(viewsets.ModelViewSet):
    queryset = TouristSpotsImage.objects.all()
    serializer_class = TouristSpotImageSerializer

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy', 'create']
        if self.action in actions:
            permissions_classes = [permissions.IsAdminUser]
        else:
            permissions_classes = [permissions.AllowAny]

        return [permission() for permission in permissions_classes]
