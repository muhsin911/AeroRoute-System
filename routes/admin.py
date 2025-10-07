# routes/admin.py
from django.contrib import admin
from .models import Airport, AirportRoute

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(AirportRoute)
class AirportRouteAdmin(admin.ModelAdmin):
    list_display = ('from_airport', 'to_airport', 'position', 'duration')
    list_filter = ('position',)
    search_fields = ('from_airport__code', 'to_airport__code')
