from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from .models import Movie, CinemaHall, Seat, Session, Ticket

User = get_user_model()

class ReservationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123',
            email='testuser@example.com'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', 
            password='password123',
            email='otheruser@example.com'
        )

        # Create Movie
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            duration_minutes=120,
            release_date=timezone.now().date()
        )

        # Create Hall
        self.hall = CinemaHall.objects.create(name="Hall 1", capacity=10)

        # Create Seats
        self.seat1 = Seat.objects.create(hall=self.hall, row="A", number=1)
        self.seat2 = Seat.objects.create(hall=self.hall, row="A", number=2)

        # Create Session
        self.session = Session.objects.create(
            movie=self.movie,
            hall=self.hall,
            start_time=timezone.now() + timezone.timedelta(days=1)
        )

        self.seats_url = reverse('session-seats', args=[self.session.id])
        self.reserve_url = reverse('session-reserve', args=[self.session.id])

        # Clear cache before each test
        cache.clear()

    def test_get_seats_status(self):
        # Authenticate not strictly required for GET seats but good practice
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.seats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Sort by id to ensure order
        data = sorted(response.data, key=lambda x: x['id'])
        self.assertEqual(data[0]['status'], 'available')

    def test_reserve_seat_success(self):
        self.client.force_authenticate(user=self.user)
        data = {'seat_id': self.seat1.id}

        response = self.client.post(self.reserve_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify lock in Redis
        lock_key = f"lock:session:{self.session.id}:seat:{self.seat1.id}"
        self.assertEqual(cache.get(lock_key), self.user.id)

        # Verify status in seats list
        response = self.client.get(self.seats_url)
        data = sorted(response.data, key=lambda x: x['id'])
        # Find seat 1
        seat_1_data = next(s for s in data if s['id'] == self.seat1.id)
        self.assertEqual(seat_1_data['status'], 'locked')

    def test_reserve_seat_conflict(self):
        # First user locks seat
        self.client.force_authenticate(user=self.user)
        self.client.post(self.reserve_url, {'seat_id': self.seat1.id})

        # Second user tries to lock same seat
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.reserve_url, {'seat_id': self.seat1.id})

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_reserve_already_purchased(self):
        # Create a ticket
        Ticket.objects.create(session=self.session, seat=self.seat1, user=self.other_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.reserve_url, {'seat_id': self.seat1.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify status in seats list
        response = self.client.get(self.seats_url)
        # Find seat 1
        seat_status = next(s for s in response.data if s['id'] == self.seat1.id)
        self.assertEqual(seat_status['status'], 'purchased')
