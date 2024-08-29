from django.db import models
from django.contrib.auth import get_user_model
from apps.tourist_spots.models import TouristSpot

User = get_user_model()

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    tourist_spot = models.ForeignKey(TouristSpot, related_name='reviews', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.tourist_spot}'
    