from django.http import JsonResponse

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.path.startswith("/api/"):
            return self.get_response(request)

        user = getattr(request, "user", None)
        session_id = request.COOKIES.get("session_id")

        if user and user.is_authenticated:
            if not user.current_session_id:
                return JsonResponse(
                    {"error": "Session expired"},
                    status=401
                )

            if str(user.current_session_id) != session_id:
                return JsonResponse(
                    {"error": "You have been logged out due to another login"},
                    status=401
                )

        return self.get_response(request)
