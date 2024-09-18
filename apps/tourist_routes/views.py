from .models import TouristRoute
from .serializers import TouristRouteSerializer, SuccessTouristRoutesResponseSerializer, ErrorTouristRoutesResponseSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .custom_persmissions import IsOwner
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


class UserTouristRoutesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TouristRouteSerializer

    @extend_schema(
        summary='Get user tourist routes',
        description='This endpoint is used to get the tourist routes of the authenticated user',
        responses={
            200: SuccessTouristRoutesResponseSerializer,
            400: ErrorTouristRoutesResponseSerializer,
            404: ErrorTouristRoutesResponseSerializer
        },
    )
    def get(self, request):
        user_routes = TouristRoute.objects.filter(user=request.user).prefetch_related('activity_routes')
        serializer = TouristRouteSerializer(user_routes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTouristRouteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TouristRouteSerializer


    def post(self, request):
        serializer = TouristRouteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateTouristRouteAPIView(APIView):
    permission_classes = [IsOwner]
    serializer_class = TouristRouteSerializer


    def put(self, request, pk):
        try:
            tourist_route = TouristRoute.objects.get(pk=pk)
        except TouristRoute.DoesNotExist:
            return Response({'error': 'Tourist route not found'}, status=status.HTTP_404_NOT_FOUND)
        
         # Comprueba los permisos en el objeto
        self.check_object_permissions(request, tourist_route)
        
        serializer = TouristRouteSerializer(tourist_route, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTouristRouteAPIView(APIView):
    permission_classes = [IsOwner]

    @extend_schema(
        summary='Delete tourist route',
        description='This endpoint is used to delete a tourist route',
        responses={
            204: SuccessTouristRoutesResponseSerializer,
            404: ErrorTouristRoutesResponseSerializer
        },
    )
    def delete(self, request, pk):
        try:
            tourist_route = TouristRoute.objects.get(pk=pk)
        except TouristRoute.DoesNotExist:
            return Response({'error': 'Tourist route not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Chek the object permissions
        self.check_object_permissions(request, tourist_route)

        # Delete the object
        tourist_route.delete()
        
        return Response({'message': 'Tourist route deleted'}, status=status.HTTP_204_NO_CONTENT)