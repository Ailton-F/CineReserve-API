from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SessionViewSet, CheckoutView, MyTicketsView

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'sessions', SessionViewSet, basename='session')

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-tickets/', MyTicketsView.as_view(), name='my_tickets'),
    path('', include(router.urls)),
]
