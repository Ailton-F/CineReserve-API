from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from .models import Movie, Session
from .serializers import MovieSerializer, SessionSerializer

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
