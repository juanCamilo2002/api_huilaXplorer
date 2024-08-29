from django.contrib import admin
from .models import Activities
# Register your models here.


class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


admin.site.register(Activities, ActivitiesAdmin)
