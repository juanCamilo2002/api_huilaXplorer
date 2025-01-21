import random
from apps.tourist_spots.models import TouristSpot
from .models import TouristRoute
from .serializers import TouristRouteSerializer, SuccessTouristRoutesResponseSerializer, ErrorTouristRoutesResponseSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .custom_persmissions import IsOwner
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2



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

class TouristRouteDetailAPIView(APIView):
    permission_classes = [IsOwner]

    @extend_schema(
        summary='Get tourist route detail',
        description='This endpoint is used to get the detail of a tourist route',
        responses={
            200: TouristRouteSerializer,
            404: ErrorTouristRoutesResponseSerializer
        },
    )
    def get(self, request, pk):
        try:
            tourist_route = TouristRoute.objects.get(pk=pk)
        except TouristRoute.DoesNotExist:
            return Response({'error': 'Tourist route not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Chek the object permissions
        self.check_object_permissions(request, tourist_route)

        serializer = TouristRouteSerializer(tourist_route)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GenerateRouteActivitiesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Obtener el usuario autenticado
        user = request.user
        preferred_activities = user.preferred_activities.all()

        # Obtener la ruta turística de la URL (por ejemplo, usando 'route_id' como parámetro)
        route_id = self.kwargs.get('route_id')
        try:
            route = TouristRoute.objects.get(id=route_id, user=user)
        except TouristRoute.DoesNotExist:
            return Response({"detail": "Ruta no encontrada o no autorizada"}, status=404)

        # Filtrar los lugares turísticos que tienen alguna de las actividades preferidas
        tourist_spots = TouristSpot.objects.filter(
            activities__in=preferred_activities
        ).distinct()

        # Generar las actividades para el rango de fechas de la ruta
        activities_for_route = self.generate_activities_for_route(route, tourist_spots, preferred_activities)

        return Response({
            'activities_for_route': activities_for_route
        })

    def generate_activities_for_route(self, route, tourist_spots, preferred_activities):
        """
        Genera actividades diarias entre las fechas de la ruta,
        distribuyendo entre 2 y 3 actividades por día dentro del horario de 6 AM a 8 PM.
        """
        activities_for_route = []
        start_date = route.date_start
        end_date = route.date_end

        # Iterar sobre los días entre date_start y date_end
        current_date = start_date
        while current_date <= end_date:
            daily_activities = self.generate_daily_activities(current_date, tourist_spots, preferred_activities)
            activities_for_route.extend(daily_activities)  # Añadimos las actividades del día directamente en la lista
            current_date += timedelta(days=1)

        return activities_for_route

    def generate_daily_activities(self, current_date, tourist_spots, preferred_activities, max_activities=3):
        """
        Genera entre 2 y 3 actividades aleatorias para un día en particular,
        priorizando lugares cercanos y ampliando el rango de búsqueda si es necesario.
        """
        daily_activities = []
        range_increase_km = 5  # Aumenta el rango en 5 km en cada iteración
        range_limit = range_increase_km  # Rango inicial de búsqueda
        selected_spots = []

        # Seleccionar un lugar inicial aleatorio para empezar
        if not tourist_spots:
            return daily_activities

        initial_spot = random.choice(tourist_spots)
        selected_spots.append(initial_spot)

        # Mientras no tengamos suficientes actividades, ampliamos el rango y buscamos lugares cercanos
        while len(selected_spots) < max_activities and range_limit <= 50:  # Limita el rango máximo a 50 km
            for spot in tourist_spots:
                if spot in selected_spots:
                    continue  # Omite los lugares ya seleccionados

                # Calcula la distancia desde el último lugar agregado
                last_spot = selected_spots[-1]
                distance = haversine_distance(last_spot.latitude, last_spot.longitude, spot.latitude, spot.longitude)

                # Agrega el lugar si está dentro del rango actual
                if distance <= range_limit:
                    selected_spots.append(spot)
                    if len(selected_spots) >= max_activities:
                        break

            range_limit += range_increase_km  # Incrementa el rango si no se alcanzó el máximo de actividades

        # Distribuir actividades entre la mañana y la tarde
        periods = [("morning", 6, 12), ("afternoon", 12, 20)]
        for i, spot in enumerate(selected_spots):
            period = periods[i % 2]
            start_hour, end_hour = period[1], period[2]

            # Filtrar las actividades en este lugar turístico
            available_activities = spot.activities.filter(id__in=preferred_activities.values_list('id', flat=True))
            if available_activities:
                selected_activity = random.choice(available_activities)

                # Asigna el horario de actividad
                activity_start_hour = random.randint(start_hour, end_hour - 1)
                start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=activity_start_hour)
                end_time = start_time + timedelta(hours=random.randint(1, 2))
                if end_time.hour > 20:
                    end_time = end_time.replace(hour=20, minute=0)

                activity = {
                    "date": start_time.strftime('%d-%m-%Y %H:%M'),
                    "activity": selected_activity.name,
                    "spot": {
                        "id": spot.id,
                        "name": spot.name,
                    },
                    "start_time": start_time.strftime('%H:%M'),
                    "end_time": end_time.strftime('%H:%M')
                }
                daily_activities.append(activity)

        return daily_activities
    

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en km
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
