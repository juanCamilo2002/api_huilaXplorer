from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ReviewSerializer
from .models import Review
from .custom_permissions import IsSelfReview
from apps.tourist_spots.models import TouristSpot
from rest_framework.decorators import action

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy']
        if self.action in actions:
            permission_classes = [IsSelfReview]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Asignar el usuario autenticado como el autor de la reseña
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        tourist_spot_id = request.query_params.get('tourist_spot', None)
        if tourist_spot_id:
            try:
                tourist_spot = TouristSpot.objects.get(id=tourist_spot_id)
                self.queryset = self.queryset.filter(tourist_spot=tourist_spot)
            except TouristSpot.DoesNotExist:
                return Response({'detail': 'Tourist spot not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='user-review')
    def retrieve_user_review(self, request):
        # Verificar si el usuario está autenticado
        if not request.user or not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Obtener el tourist_spot_id desde los parámetros de consulta
        tourist_spot_id = request.query_params.get('tourist_spot')
        
        if not tourist_spot_id:
            return Response({'detail': 'Tourist spot ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verificar si existe el lugar turístico
            tourist_spot = TouristSpot.objects.get(id=tourist_spot_id)
        except TouristSpot.DoesNotExist:
            return Response({'detail': 'Tourist spot not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Buscar la reseña del usuario sobre el lugar turístico
        review = Review.objects.filter(user=request.user, tourist_spot=tourist_spot).first()
        if review:
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No review found for this user on the specified tourist spot.'}, status=status.HTTP_404_NOT_FOUND)

