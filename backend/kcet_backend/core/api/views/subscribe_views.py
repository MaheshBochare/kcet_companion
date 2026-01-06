from core.services.subscription_service import SubscriptionService
import re
import json
from django.http import JsonResponse

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

def subscribe(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid HTTP method"}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    email = data.get("email", "").strip()

    # 🧠 Business decision #1: Validate email
    if not re.match(EMAIL_REGEX, email):
        return JsonResponse({"status": "error", "message": "Invalid email format"}, status=400)

    service = SubscriptionService()
    result = service.subscribe(email)

    # 🧠 Business decision #2: Customize response
    if result["created"]:
        msg = "Subscription created. Approval pending."
        code = 201
    else:
        msg = "You are already subscribed."
        code = 200

    return JsonResponse({"status": "success", "message": msg}, status=code)
