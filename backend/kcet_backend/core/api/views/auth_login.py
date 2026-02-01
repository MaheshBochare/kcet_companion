from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import uuid

from core.models import User


@method_decorator(csrf_exempt, name="dispatch")
class VerifyOTPView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        # 1️⃣ Validate input
        if not email or not otp:
            return Response({"error": "Email and OTP are required"}, status=400)

        email = email.strip().lower()
        otp = str(otp).strip()

        # 2️⃣ Find user
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        # 3️⃣ OTP validity
        if not user.otp or not user.otp_expires_at:
            return Response({"error": "OTP expired"}, status=400)

        if user.otp_expires_at < timezone.now():
            return Response({"error": "OTP expired"}, status=400)

        if user.otp != otp:
            return Response({"error": "Invalid OTP"}, status=400)

        # 4️⃣ SINGLE ACTIVE SESSION
        session_id = uuid.uuid4()
        user.current_session_id = session_id
        user.otp = None
        user.otp_expires_at = None
        user.last_login = timezone.now()
        user.save(update_fields=[
            "current_session_id",
            "otp",
            "otp_expires_at",
            "last_login"
        ])

        # 5️⃣ JWT
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        refresh["session_id"] = str(session_id)

        response = Response(
            {
                "message": "Login successful",
                "role": user.role,
            },
            status=200
        )

        # 🔐 Access token (HTTP-only)
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,      # True in production
            samesite="Lax",
            max_age=60 * 60
        )

        # 🔑 SESSION ID (readable by middleware / frontend)
        response.set_cookie(
            key="session_id",
            value=str(session_id),
            httponly=False,    # frontend & middleware can read
            secure=False,      # True in production
            samesite="Lax",
            max_age=60 * 60
        )

        return response
