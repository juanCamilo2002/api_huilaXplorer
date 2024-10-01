from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import EventSpotSerializer
from .models import EventSpot
from apps.tourist_spots.models import TouristSpot


class EventSpotViewSet(viewsets.ModelViewSet):
    queryset = EventSpot.objects.all()
    serializer_class = EventSpotSerializer

    def get_permissions(self):
        actions = ['list', 'retrieve']

        if self.action in actions:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        tourist_spot_id = request.query_params.get('tourist_spot', None)
        if tourist_spot_id:
            try:
                tourist_spot = TouristSpot.objects.get(id=tourist_spot_id)
                self.queryset = self.queryset.filter(tourist_spot=tourist_spot)
            except TouristSpot.DoesNotExist:
                return Response({'detail': 'Tourist spot not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return super().list(request, *args, **kwargs)