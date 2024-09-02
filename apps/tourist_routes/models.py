from django.db import models
from django.contrib.auth import get_user_model
from apps.tourist_spots.models import TouristSpot

User = get_user_model()


class TouristRoute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_start = models.DateField()
    date_end = models.DateField()
    user = models.ForeignKey(User, related_name='tourist_routes' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class ActivityRoute(models.Model):
    date = models.DateTimeField()
    tourist_spot = models.ForeignKey(TouristSpot, related_name='activity_routes', on_delete=models.CASCADE)
    route = models.ForeignKey(TouristRoute, related_name='activity_routes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tourist_spot.name} - {self.route.name}'