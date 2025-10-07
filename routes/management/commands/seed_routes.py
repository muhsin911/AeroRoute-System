from django.core.management.base import BaseCommand

# Import Airport and AirportRoute models from routes app
from routes.models import Airport, AirportRoute


class Command(BaseCommand):
    """
    Custom Django management command to seed the database with
    demo data consisting of airports and their directed routes.

    Usage: python manage.py seed_routes
    """

    help = "Seed demo airports and routes"

    def handle(self, *args, **options):
        """
        Command entry point executed when running the 'seed_routes' command.

        Creates or gets airports A, B, and C with codes and names.

        Creates or updates two routes emanating from Airport A:
          - Left child route to Airport B with duration 150
          - Right child route to Airport C with duration 250

        Prints success message once seeding is done.
        """
        # Create or get Airport A (code='A')
        A, _ = Airport.objects.get_or_create(
            code='A', defaults={'name': 'Airport A'}
        )

        # Create or get Airport B (code='B')
        B, _ = Airport.objects.get_or_create(
            code='B', defaults={'name': 'Airport B'}
        )

        # Create or get Airport C (code='C')
        C, _ = Airport.objects.get_or_create(
            code='C', defaults={'name': 'Airport C'}
        )

        # Create or update route from Airport A to B as left child with duration 150
        AirportRoute.objects.update_or_create(
            from_airport=A,
            position='left',
            defaults={'to_airport': B, 'duration': 150}
        )

        # Create or update route from Airport A to C as right child with duration 250
        AirportRoute.objects.update_or_create(
            from_airport=A,
            position='right',
            defaults={'to_airport': C, 'duration': 250}
        )

        # Output success message to the terminal
        self.stdout.write(self.style.SUCCESS('Seeded airports and routes'))
