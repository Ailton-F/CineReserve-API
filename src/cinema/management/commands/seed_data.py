from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from cinema.models import Movie, CinemaHall, Seat, Session
from cinema.factories import MovieFactory, CinemaHallFactory, SeatFactory, SessionFactory
import random

class Command(BaseCommand):
    help = 'Seeds the database with mock movies, halls, seats and sessions.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if Movie.objects.exists() or CinemaHall.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Skipping seeding.'))
            return

        self.stdout.write('Seeding data...')

        # 1. Create Movies
        self.stdout.write('Creating 5 movies...')
        movies = MovieFactory.create_batch(5)

        # 2. Create Cinema Halls and Seats
        self.stdout.write('Creating 3 halls with 50 seats each...')
        halls = []
        for i in range(3):
            hall = CinemaHallFactory.create(name=f"Hall {i+1}", capacity=50)
            halls.append(hall)
            
            # Create seats for each hall (5 rows of 10)
            seats = []
            for r in ['A', 'B', 'C', 'D', 'E']:
                for n in range(1, 11):
                    seats.append(Seat(hall=hall, row=r, number=n))
            Seat.objects.bulk_create(seats)

        # 3. Create Sessions
        self.stdout.write('Creating sessions for the next 3 days...')
        now = timezone.now()
        for movie in movies:
            for hall in halls:
                # 2 sessions per movie per hall
                SessionFactory.create(
                    movie=movie,
                    hall=hall,
                    start_time=now + timezone.timedelta(days=random.randint(1, 3), hours=random.randint(1, 23))
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
