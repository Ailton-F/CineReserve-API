from rest_framework import serializers
from .models import Movie, CinemaHall, Session, Seat, Ticket

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row', 'number']

class SeatStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    row = serializers.CharField()
    number = serializers.IntegerField()
    status = serializers.ChoiceField(choices=['available', 'locked', 'purchased'])

class ReservationSerializer(serializers.Serializer):
    seat_id = serializers.IntegerField()

class CheckoutSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'session', 'seat', 'user', 'purchased_at', 'digital_id']
        read_only_fields = ['id', 'user', 'purchased_at', 'digital_id']

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
