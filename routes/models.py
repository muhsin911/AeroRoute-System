from django.db import models
from django.core.validators import ValidationError

# Create your models here.
class Airport(models.Model):
    """
    Airport model holds a unique airport code and human-readable name.
    """
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"
    

class AirportRoute(models.Model):
    """
    Directed route from one airport to another.
    Each 'from_airport' can have at most one 'left' and one 'right' child.
    """
    LEFT = 'left'
    RIGHT = 'right'
    POSITION_CHOICES = [
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
    ]

    from_airport = models.ForeignKey(Airport, related_name='routes_from', on_delete=models.CASCADE)
    to_airport = models.ForeignKey(Airport, related_name='routes_to', on_delete=models.CASCADE)
    position = models.CharField(max_length=5, choices=POSITION_CHOICES)
    duration = models.PositiveIntegerField(help_text='Distance in km (or duration in minutes)')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_airport', 'position'], name='unique_position_per_from_airport')
        ]
        ordering = ['from_airport', 'position']

    def clean(self):
        # Prevent a route that goes from an airport to itself
        if self.from_airport_id == self.to_airport_id:
            raise ValidationError("from_airport and to_airport must be different")

    def __str__(self):
        return f"{self.from_airport.code} -> {self.to_airport.code} ({self.position}, {self.duration} km)"