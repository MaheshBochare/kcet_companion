from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from core.models import College


@cache_page(60 * 30)  # Cache for 30 minutes
def featured_colleges(request):
    colleges = (
        College.objects
        .only("College_name", "location", "highestpackage", "naaccrating")
        .order_by("-naaccrating", "-highestpackage")[:6]
    )

    result = []
    for c in colleges:
        result.append({
            "name": c.College_name,
            "location": c.location,
            "naac": c.naaccrating,
            "highest_package": c.highestpackage,
        })

    return JsonResponse({"featured_colleges": result})
import uuid
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from core.infrastructure.django_models.roles import User
from core.utils.otplogic import set_otp

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        set_otp(user)
        return Response({"message": "OTP sent"})

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        user = User.objects.filter(email=email, otp=otp).first()
        if not user or user.otp_expiry < timezone.now():
            return Response({"error": "Invalid OTP"}, status=400)

        session_id = uuid.uuid4()
        user.current_session_id = session_id
        user.otp = None
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh["session_id"] = str(session_id)

        response = Response({"role": user.role})

        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            samesite="Lax",
        )

        response.set_cookie(
            "session_id",
            str(session_id),
            httponly=False,
        )

        return response
