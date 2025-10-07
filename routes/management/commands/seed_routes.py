# routes/management/commands/seed_routes.py
from django.core.management.base import BaseCommand
from routes.models import Airport, AirportRoute

class Command(BaseCommand):
    help = "Seed demo airports and routes"

    def handle(self, *args, **options):
        A, _ = Airport.objects.get_or_create(code='A', defaults={'name': 'Airport A'})
        B, _ = Airport.objects.get_or_create(code='B', defaults={'name': 'Airport B'})
        C, _ = Airport.objects.get_or_create(code='C', defaults={'name': 'Airport C'})

        AirportRoute.objects.update_or_create(from_airport=A, position='left', defaults={'to_airport': B, 'duration': 150})
        AirportRoute.objects.update_or_create(from_airport=A, position='right', defaults={'to_airport': C, 'duration': 250})

        self.stdout.write(self.style.SUCCESS('Seeded airports and routes'))
