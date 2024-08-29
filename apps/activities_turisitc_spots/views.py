from rest_framework import viewsets
from .models import Activities
from .serializers import ActivitiesSerializer
from rest_framework import permissions


class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer

    def get_permissions(self):
        actions = ['list', 'retrieve']

        if self.action in actions:
            permissions_classes = [permissions.AllowAny]
        else:
            permissions_classes = [permissions.IsAdminUser]

        return [permission() for permission in permissions_classes]
