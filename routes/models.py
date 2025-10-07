from django.db import models
from django.core.validators import ValidationError


# Define the Airport model representing an airport entity with unique code and name
class Airport(models.Model):
    """
    Airport model holds a unique airport code and human-readable name.
    """

    # Unique airport code (e.g. 'JFK', 'LHR', max length 10 chars)
    code = models.CharField(max_length=10, unique=True)

    # Descriptive name for the airport (e.g. 'John F Kennedy International Airport')
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        String representation of an Airport instance,
        returns string like 'JFK - John F Kennedy International Airport'.
        """
        return f"{self.code} - {self.name}"


# Define the AirportRoute model representing a directed flight route from one airport to another
class AirportRoute(models.Model):
    """
    Directed route from one airport to another.
    Each 'from_airport' can have at most one 'left' and one 'right' child.
    """

    # Constants for direction/position choices (left or right child node)
    LEFT = 'left'
    RIGHT = 'right'

    POSITION_CHOICES = [
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
    ]

    # ForeignKey to the source airport (this route originates here)
    # Multiple routes from the same airport allowed (related_name='routes_from')
    from_airport = models.ForeignKey(
        Airport, related_name='routes_from', on_delete=models.CASCADE
    )

    # ForeignKey to the destination airport (this route points to here)
    to_airport = models.ForeignKey(
        Airport, related_name='routes_to', on_delete=models.CASCADE
    )

    # Direction of the route relative to 'from_airport': left or right child
    position = models.CharField(max_length=5, choices=POSITION_CHOICES)

    # Duration or distance of the route in kilometers (positive integer)
    duration = models.PositiveIntegerField(help_text='Distance in km (or duration in minutes)')

    class Meta:
        # Constraint to ensure only one route per position (left or right) from a given airport
        constraints = [
            models.UniqueConstraint(
                fields=['from_airport', 'position'],
                name='unique_position_per_from_airport'
            )
        ]
        # Default ordering by source airport and position for querysets
        ordering = ['from_airport', 'position']

    def clean(self):
        """
        Custom model validation:
        Prevent a route where the source and destination airport are the same.
        Raises ValidationError if violated.
        """
        if self.from_airport_id == self.to_airport_id:
            raise ValidationError("from_airport and to_airport must be different")

    def __str__(self):
        """
        String representation of an AirportRoute instance,
        e.g. 'JFK -> LHR (left, 4500 km)'
        """
        return f"{self.from_airport.code} -> {self.to_airport.code} ({self.position}, {self.duration} km)"
