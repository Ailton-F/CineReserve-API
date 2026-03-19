from rest_framework import serializers
from .models import Movie, CinemaHall, Session, Seat

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    hall = CinemaHallSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=CinemaHall.objects.all(), source='hall', write_only=True
    )

    class Meta:
        model = Session
        fields = ['id', 'movie', 'hall', 'start_time', 'movie_id', 'hall_id']
