from django.db import models
from apps.activities_turisitc_spots.models import Activities


class LocationSpot(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TouristSpot(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    location = models.ForeignKey(LocationSpot, related_name='tourist_spots', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=False, null=False)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, default=0)
    num_reviews = models.IntegerField(default=0, blank=True, null=True)
    activities = models.ManyToManyField(Activities, related_name='tourist_spots')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    
class TouristSpotsImage(models.Model):
    tourist_spot = models.ForeignKey(TouristSpot, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tourist_spots/')
    caption = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.tourist_spot.name} -  {self.caption}"