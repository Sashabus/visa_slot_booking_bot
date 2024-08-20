# webhook/views.py
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .signals import handle_calendly_event


@method_decorator(csrf_exempt, name='dispatch')
class CalendlyWebhookView(View):
    """
    Handle incoming webhooks from Calendly.
    """

    def post(self, request, *args, **kwargs):
        try:
            # Parse the incoming JSON data
            payload = json.loads(request.body)

            # Handle the specific Calendly event (e.g., invitee.created)
            handle_calendly_event(payload)

            # Return a 200 OK response
            return JsonResponse({"status": "success"}, status=200)

        except json.JSONDecodeError:
            # Return a 400 Bad Request if the JSON is invalid
            return HttpResponseBadRequest("Invalid JSON")

        except Exception as e:
            # Log the error and return a 500 Internal Server Error
            return JsonResponse({"error": str(e)}, status=500)
