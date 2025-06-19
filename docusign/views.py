from django.shortcuts import render

# Create your views here.
# docusign/views.py

from django.http import JsonResponse
from .utils import generate_access_token, send_docusign_envelope

def send_float_plan(request):
    if request.method == "POST":
        # Get recipient details from the request (e.g., form data or JSON payload)
        recipient_email = request.POST.get("email", "user@example.com")  # Default email for testing
        recipient_name = request.POST.get("name", "User Name")  # Default name for testing

        try:
            # Send the envelope
            envelope_id = send_docusign_envelope(recipient_email, recipient_name)
            return JsonResponse({"status": "success", "envelope_id": envelope_id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)