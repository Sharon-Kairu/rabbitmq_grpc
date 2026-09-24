import time
from celery import shared_task
from models import Booking

@shared_task
def send_booking_confirmation(booking_id):
    # Simulates a slow operation, e.g. sending an SMS/email confirmation
    time.sleep(5)
    booking = Booking.objects.get(id=booking_id)
    booking.status = "confirmed"
    booking.save()
    print(f"[CELERY] Confirmation sent for booking #{booking.id} — {booking.patient_name}")