from rest_framework import viewsets, permissions, filters
from .models import Activities
from .serializers import ActivitiesSerializer


class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        actions = ['list', 'retrieve']

        if self.action in actions:
            permissions_classes = [permissions.AllowAny]
        else:
            permissions_classes = [permissions.IsAdminUser]

        return [permission() for permission in permissions_classes]
