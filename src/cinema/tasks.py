import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Ticket

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task
def send_ticket_confirmation_email(ticket_id):
    try:
        ticket = Ticket.objects.select_related('user', 'session__movie', 'session__hall', 'seat').get(id=ticket_id)
        user = ticket.user

        message = (
            f"Hello {user.username},\n\n"
            f"Your booking for '{ticket.session.movie.title}' is confirmed!\n"
            f"Time: {ticket.session.start_time}\n"
            f"Hall: {ticket.session.hall.name}\n"
            f"Seat: {ticket.seat.row}{ticket.seat.number}\n"
            f"Ticket ID: {ticket.digital_id}\n\n"
            "Enjoy the movie!"
        )
        
        logger.info(f"MOCK EMAIL SENT TO {user.email}:\n{message}")
        return True
    except Ticket.DoesNotExist:
        logger.error(f"Ticket {ticket_id} not found for confirmation email.")
        return False
