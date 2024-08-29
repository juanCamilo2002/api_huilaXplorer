from django.contrib import admin
from .models import EventSpot
# Register your models here.
class EventSpotInline(admin.TabularInline):
    model = EventSpot
    extra = 1
    fields = ['name', 'date']


class EventSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name', 'description')


admin.site.register(EventSpot, EventSpotAdmin)