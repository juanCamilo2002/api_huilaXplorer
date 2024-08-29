from django.db import models
from apps.tourist_spots.models import TouristSpot
# Create your models here.


class EventSpot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    tourist_spot = models.ForeignKey(
        TouristSpot, related_name='events', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name