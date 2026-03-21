import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from .models import Movie, CinemaHall, Seat, Session

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    duration_minutes = factory.Faker('random_int', min=80, max=180)
    release_date = factory.Faker('date_between', start_date='-2y', end_date='today')
    poster_url = factory.Faker('image_url')

class CinemaHallFactory(DjangoModelFactory):
    class Meta:
        model = CinemaHall

    name = factory.Sequence(lambda n: f"Hall {n+1}")
    capacity = 100 # Default but can be overridden

class SeatFactory(DjangoModelFactory):
    class Meta:
        model = Seat

    hall = factory.SubFactory(CinemaHallFactory)
    row = factory.Iterator(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
    number = factory.Sequence(lambda n: (n % 10) + 1)

class SessionFactory(DjangoModelFactory):
    class Meta:
        model = Session

    movie = factory.SubFactory(MovieFactory)
    hall = factory.SubFactory(CinemaHallFactory)
    start_time = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=1))
