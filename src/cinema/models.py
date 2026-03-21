import uuid
from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    release_date = models.DateField()
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Seat(models.Model):
    hall = models.ForeignKey(CinemaHall, related_name='seats', on_delete=models.CASCADE)
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hall', 'row', 'number')

    def __str__(self):
        return f"{self.hall.name} - {self.row}{self.number}"

class Session(models.Model):
    movie = models.ForeignKey(Movie, related_name='sessions', on_delete=models.CASCADE)
    hall = models.ForeignKey(CinemaHall, related_name='sessions', on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.hall.name} ({self.start_time})"

class Ticket(models.Model):
    session = models.ForeignKey(Session, related_name='tickets', on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name='tickets', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets', on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    digital_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        unique_together = ('session', 'seat')

    def __str__(self):
        return f"Ticket for {self.user.username} - {self.session.movie.title}"
