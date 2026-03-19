from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Movie, Session, Seat, Ticket
from .serializers import MovieSerializer, SessionSerializer, SeatStatusSerializer, ReservationSerializer

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all().order_by('release_date')
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key = 'movie_list'
        data = cache.get(cache_key)
        
        if not data:
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(cache_key, data, 60 * 15)  # Cache for 15 minutes
        
        return Response(data)

    @action(detail=True, methods=['get'])
    def sessions(self, request, pk=None):
        cache_key = f'movie_sessions_{pk}'
        data = cache.get(cache_key)
        
        if not data:
            movie = self.get_object()
            sessions = Session.objects.filter(movie=movie).order_by('start_time')
            serializer = SessionSerializer(sessions, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60 * 15)
            
        return Response(data)

class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.all().order_by('start_time')
    serializer_class = SessionSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def seats(self, request, pk=None):
        """
        Get all seats for this session with their current status.
        Status: 'available', 'locked', 'purchased'
        """
        session = self.get_object()
        seats = Seat.objects.filter(hall=session.hall)
        
        # Get all purchased tickets for this session
        purchased_tickets = Ticket.objects.filter(session=session).values_list('seat_id', flat=True)
        purchased_seat_ids = set(purchased_tickets)
        
        seat_data = []
        for seat in seats:
            status_label = 'available'
            
            # Check DB (Purchased)
            if seat.id in purchased_seat_ids:
                status_label = 'purchased'
            else:
                # Check Redis (Locked)
                lock_key = f"lock:session:{session.id}:seat:{seat.id}"
                locked_by = cache.get(lock_key)
                if locked_by:
                    status_label = 'locked'
            
            seat_data.append({
                'id': seat.id,
                'row': seat.row,
                'number': seat.number,
                'status': status_label
            })
            
        serializer = SeatStatusSerializer(seat_data, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reserve(self, request, pk=None):
        """
        Attempt to lock a seat for the authenticated user.
        """
        session = self.get_object()
        serializer = ReservationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        seat_id = serializer.validated_data['seat_id']
        seat = get_object_or_404(Seat, id=seat_id, hall=session.hall)
        
        # 1. Check if seat is already purchased
        if Ticket.objects.filter(session=session, seat=seat).exists():
            return Response(
                {'detail': 'Seat already purchased.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 2. Check if seat is locked in Redis
        lock_key = f"lock:session:{session.id}:seat:{seat.id}"
        locked_by = cache.get(lock_key)
        
        if locked_by:
            # If locked by the current user, extend the lock
            if locked_by == request.user.id:
                cache.set(lock_key, request.user.id, timeout=600)
                return Response({'detail': 'Lock extended.'}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'detail': 'Seat is currently locked by another user.'},
                    status=status.HTTP_409_CONFLICT
                )
        
        # 3. Create a new lock (10 minutes TTL)
        cache.set(lock_key, request.user.id, timeout=600)
        
        return Response({'detail': 'Seat locked successfully.'}, status=status.HTTP_201_CREATED)
