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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
import uuid


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response(
                {"error": "Email and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email, otp=otp).first()

        if not user or not user.otp_expires_at or user.otp_expires_at < timezone.now():
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔐 SINGLE ACTIVE SESSION (IMPORTANT)
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

        # 🔑 JWT with session_id embedded
        refresh = RefreshToken.for_user(user)
        refresh["session_id"] = str(session_id)

        response = Response(
            {
                "role": user.role,
                "email": user.email,
                "session_id": str(session_id)
            },
            status=status.HTTP_200_OK
        )

        # 🔐 Access token (HTTP-only)
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            samesite="Lax",
            secure=False,  # True in production (HTTPS)
        )

        # 🔐 Session ID (readable by frontend)
        response.set_cookie(
            key="session_id",
            value=str(session_id),
            httponly=False,
            samesite="Lax",
            secure=False,  # True in production
        )

        return response
