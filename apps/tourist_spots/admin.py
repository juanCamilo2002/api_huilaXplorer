from django.contrib import admin
from .models import TouristSpot, TouristSpotsImage
from apps.events_spots.admin import EventSpotInline
from apps.reviews.admin import ReviewTabularInline
# Register your models here.

class TouristSpotImageInline(admin.TabularInline):
    model = TouristSpotsImage
    extra = 1
    fields = ['image', 'caption']

class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude')
    search_fields = ('name', 'description')
    inlines = [TouristSpotImageInline, EventSpotInline, ReviewTabularInline]


admin.site.register(TouristSpot, TouristSpotAdmin)