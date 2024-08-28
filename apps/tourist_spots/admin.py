from django.contrib import admin
from .models import TouristSpot, TouristSpotsImage
# Register your models here.

class TouristSpotImageInline(admin.TabularInline):
    model = TouristSpotsImage
    extra = 1
    fields = ['image', 'caption']

class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude')
    search_fields = ('name', 'description')
    inlines = [TouristSpotImageInline]


admin.site.register(TouristSpot, TouristSpotAdmin)