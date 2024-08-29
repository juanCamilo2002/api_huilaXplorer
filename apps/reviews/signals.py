from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from django.db.models import Avg



@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_tourist_spot_reviews(sender, instance, **kwargs):

    # Get the tourist spot related to the review
    tourist_spot = instance.tourist_spot

    # Get the number of reviews for the tourist spot and average rating
    num_reviews = Review.objects.filter(tourist_spot=tourist_spot).count()
    average_rating = Review.objects.filter(tourist_spot=tourist_spot).aggregate(Avg('rating'))['rating__avg']

    # Update the tourist spot with the new values
    tourist_spot.num_reviews = num_reviews
    tourist_spot.average_rating = average_rating if average_rating is not None else 0
    tourist_spot.save()
