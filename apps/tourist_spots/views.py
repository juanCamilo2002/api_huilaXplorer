from rest_framework import viewsets, permissions, filters
from .models import TouristSpot, TouristSpotsImage, LocationSpot
from .serializers import TouristSpotImageSerializer, TouristSpotSerializer, LocationSpotSerializer

class LocationSoptViewSet(viewsets.ModelViewSet):
    queryset = LocationSpot.objects.all()
    serializer_class = LocationSpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

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
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'latitude', 'longitude', 'location__name']

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
