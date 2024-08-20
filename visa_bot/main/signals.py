# webhook/signals.py
from django.dispatch import Signal

# Define custom signals for handling Calendly and Telegram events
calendly_event_received = Signal(providing_args=["payload"])


def handle_calendly_event(payload):
    # Send a signal when a Calendly event is received
    calendly_event_received.send(sender=None, payload=payload)
