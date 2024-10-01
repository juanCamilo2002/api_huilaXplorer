from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ReviewSerializer
from .models import Review
from .custom_permissions import IsSelfReview
from apps.tourist_spots.models import TouristSpot


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy']
        if self.action in actions:
            permissions_classes = [IsSelfReview]
        else:
            permissions_classes = [permissions.AllowAny]

        return [permission() for permission in permissions_classes]

    def list(self, request, *args, **kwargs):
        tourist_spot_id = request.query_params.get('tourist_spot', None)
        if tourist_spot_id:
            try:
                tourist_spot = TouristSpot.objects.get(id=tourist_spot_id)
                self.queryset = self.queryset.filter(tourist_spot=tourist_spot)
            except TouristSpot.DoesNotExist:
                return Response({'detail': 'Tourist spot not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return super().list(request, *args, **kwargs)
