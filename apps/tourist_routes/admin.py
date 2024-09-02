from django.contrib import admin
from .models import TouristRoute, ActivityRoute


class ActivityRouteInline(admin.TabularInline):
    model = ActivityRoute
    extra = 1
    fields = ['date', 'tourist_spot']


class TouristRouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date_start', 'date_end')
    search_fields = ('name', 'description')
    inlines = [ActivityRouteInline]


admin.site.register(TouristRoute, TouristRouteAdmin)