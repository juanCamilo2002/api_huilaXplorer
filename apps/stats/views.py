from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from datetime import timedelta
from django.utils import timezone
from apps.tourist_spots.models import TouristSpot
from apps.activities_turisitc_spots.models import Activities

User = get_user_model()


class UserAccountMonthlyStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary='Get user account monthly stats',
        description='This endpoint is used to get the monthly stats of the user accounts',
    )
    def get(self, request):

         # Diccionario con nombres de los meses en español
        month_names = {
            1: "enero",
            2: "febrero",
            3: "marzo",
            4: "abril",
            5: "mayo",
            6: "junio",
            7: "julio",
            8: "agosto",
            9: "septiembre",
            10: "octubre",
            11: "noviembre",
            12: "diciembre",
        }

        # Obtener el año del query param (si no se proporciona, será None)
        year = request.query_params.get('year', None)

        if year:
            # Filtro para el año proporcionado en el query param
            users = User.objects.filter(created_at__year=year)
            stats = users.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

            # Inicializar diccionario para cada mes del año solicitado
            months_stats = {f'{month_names[month]} {year}': 0 for month in range(1, 13)}
            for stat in stats:
                month = stat['month'].month
                months_stats[f'{month_names[month]} {year}'] = stat['count']

        else:
            # Calcular la fecha de hace 12 meses desde hoy
            today = timezone.now()
            last_year_date = today - timedelta(days=365)

            # Filtrar los usuarios creados en los últimos 12 meses
            users = User.objects.filter(created_at__gte=last_year_date)
            stats = users.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

            months_stats = {}
            for i in range(11, -1, -1):
                month_date = today - timedelta(days=i * 30)
                month_name = month_names[month_date.month]
                year = month_date.year
                months_stats[f'{month_name} {year}'] = 0

            for stat in stats:
                month = stat['month'].month
                year = stat['month'].year
                month_name = month_names[month]
                months_stats[f'{month_name} {year}'] = stat['count']

        # Ordenar los meses y años cronológicamente
        ordered_stats = dict(sorted(months_stats.items(), key=lambda x: (int(x[0].split()[1]), list(month_names.values()).index(x[0].split()[0]))))

        return Response({
            'results': ordered_stats
        }, status=status.HTTP_200_OK)
    

class TopTouristSpotsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
         # Consulta para contar cuántas rutas contiene cada TouristSpot
        top_spots = (
            TouristSpot.objects.annotate(route_count=Count('activity_routes__route'))
            .order_by('-route_count')[:5]
        )

        # Preparar la respuesta
        results = [
            {
                'id': spot.id,  # Accediendo al atributo 'id' de cada objeto TouristSpot
                'name': spot.name,
                'route_count': spot.route_count,
                'location': spot.location.name if spot.location else None,  # Suponiendo que 'location' puede ser None
            }
            for spot in top_spots  # Asegúrate de que estás iterando sobre cada objeto del QuerySet
        ]

        return Response({'top_tourist_spots': results}, status=status.HTTP_200_OK)
    

class TopActivitiesAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        # Contar cuantas veces cada actividad ha sido preferida por los usuarios
        top_activities = (
            Activities.objects.annotate(user__count=Count('preferred_activities')).order_by('-user__count')[:5]
        )

        # Preparar la respuesta
        results = [
            {
                'id': activity.id,
                'name': activity.name,
                'user_count': activity.user__count,
            }
            for activity in top_activities
        ]

        return Response({'results': results}, status=status.HTTP_200_OK)


class TopRatedTouristSpotsAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
         # Filtrar los 5 lugares turísticos con el mayor average_rating
        top_spots = TouristSpot.objects.order_by('-average_rating')[:5]

        # Preparamos los resultados
        results = [
            {
                'id': spot.id,
                'name': spot.name,
                'average_rating': spot.average_rating,  # Usamos el campo average_rating del modelo
                'num_reviews': spot.num_reviews  # Usamos el campo num_reviews del modelo
            }
            for spot in top_spots
        ]

        return Response({'results': results}, status=status.HTTP_200_OK)