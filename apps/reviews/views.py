from rest_framework import viewsets, permissions
from .serializers import ReviewSerializer
from .models import Review
from .custom_permissions import IsSelfReview


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
