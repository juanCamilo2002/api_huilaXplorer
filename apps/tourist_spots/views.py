from rest_framework import viewsets, permissions, filters
from .models import TouristSpot, TouristSpotsImage, LocationSpot
from rest_framework.response import Response
from .serializers import TouristSpotImageSerializer, TouristSpotSerializer, LocationSpotSerializer

class LocationSpotViewSet(viewsets.ModelViewSet):
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

    def list(self, request, *args, **kwargs):
        # Comprobar si se solicita obtener todos los registros
        if request.query_params.get('all') == 'true':
            # Si se solicita, devolver todos los registros
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({"results": serializer.data})
        
        # Si no se solicita, seguir con el comportamiento predeterminado (paginado)
        return super().list(request, *args, **kwargs)


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
