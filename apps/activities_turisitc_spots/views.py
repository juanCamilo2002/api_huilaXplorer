from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
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

    def list(self, request, *args, **kwargs):
        # Comprobar si se solicita obtener todos los registros
        if request.query_params.get('all') == 'true':
            # Si se solicita, devolver todos los registros
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({"results": serializer.data})
        
        # Si no se solicita, seguir con el comportamiento predeterminado (paginado)
        return super().list(request, *args, **kwargs)