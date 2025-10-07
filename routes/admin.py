from django.contrib import admin
from .models import Airport, AirportRoute


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    """
    Admin interface for Airport model.

    list_display:
      Shows 'code' and 'name' columns in the list view for quick reference.

    search_fields:
      Enables search box to filter airports by 'code' or 'name'.
    """
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(AirportRoute)
class AirportRouteAdmin(admin.ModelAdmin):
    """
    Admin interface for AirportRoute model.

    list_display:
      Displays key route details - source & destination airports, position, and duration.

    list_filter:
      Adds filter sidebar to allow narrowing routes by 'position' (left/right).

    search_fields:
      Enables searching routes by the codes of source or destination airports
      with double underscore lookup through foreign keys.
    """
    list_display = ('from_airport', 'to_airport', 'position', 'duration')
    list_filter = ('position',)
    search_fields = ('from_airport__code', 'to_airport__code')
