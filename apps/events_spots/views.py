from rest_framework import viewsets, permissions
from .serializers import EventSpotSerializer
from .models import EventSpot


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
