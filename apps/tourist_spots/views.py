import django_filters
from rest_framework import viewsets, permissions, filters
from .models import TouristSpot, TouristSpotsImage, LocationSpot
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TouristSpotImageSerializer, TouristSpotSerializer, LocationSpotSerializer
from django_filters.rest_framework import DjangoFilterBackend
import random

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

class TouristSpotFilter(django_filters.FilterSet):
    # Filtros específicos por campos que quieras incluir
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.NumberFilter(field_name="location__id")
    activity = django_filters.NumberFilter(field_name="activities__id")
    latitude = django_filters.NumberFilter()
    longitude = django_filters.NumberFilter()
    average_rating = django_filters.NumberFilter()

    class Meta:
        model = TouristSpot
        fields = ['name', 'description', 'location', 'activity', 'latitude', 'longitude', 'average_rating']

class TouristSpotViewSet(viewsets.ModelViewSet):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description', 'latitude', 'longitude', 'location__name']
    filterset_class = TouristSpotFilter

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

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)
        
        # Obtener los parámetros opcionales para filtrar
        location_id = request.query_params.get('location_id')
        activity_id = request.query_params.get('activity_id')

        # Filtrar los spots basados en las preferencias del usuario
        spots = TouristSpot.objects.all()

        # Filtrar por location si se proporciona un ID específico
        if location_id and location_id != "all":
            spots = spots.filter(location_id=location_id)
        
        # Filtrar por activity si se proporciona un ID específico
        if activity_id and activity_id != "all":
            spots = spots.filter(activities__id=activity_id).distinct()

        # Si ambos son "all", no se filtran por location ni activity
        if (location_id == "all") and (activity_id == "all"):
            # Aquí se podrían incluir recomendaciones basadas en preferencias
            preferred_activities = user.preferred_activities.all()
            if preferred_activities.exists():
                spots = spots.filter(activities__in=preferred_activities).distinct()

        # Verificar si hay spots recomendados
        if spots.exists():
            # Seleccionar aleatoriamente hasta 10 lugares
            spots = random.sample(list(spots), min(len(spots), 10))
        else:
            # Si no hay lugares según las preferencias, elegir 10 aleatorios de todos los lugares
            spots = random.sample(list(TouristSpot.objects.all()), min(len(TouristSpot.objects.all()), 10))

        # Serializar los resultados
        serializer = self.get_serializer(spots, many=True)
        return Response({"results": serializer.data})

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
