from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail
import random

from core.models import User


class ResendOTPView(APIView):
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email required"}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        # Prevent spam (1 OTP per minute)
        if user.otp_expires_at and user.otp_expires_at > timezone.now() - timezone.timedelta(minutes=4):
            return Response(
                {"error": "Please wait before requesting another OTP"},
                status=429
            )

        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
        user.save(update_fields=["otp", "otp_expires_at"])

        send_mail(
            "KCET Login OTP",
            f"Your OTP is {otp}",
            "kcetcompanion@gmail.com",
            [email],
        )

        return Response({"message": "OTP resent successfully"})
