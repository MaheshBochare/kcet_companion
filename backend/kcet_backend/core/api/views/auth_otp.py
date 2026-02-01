from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random

from core.models import User


@method_decorator(csrf_exempt, name="dispatch")
class SendOTPView(APIView):
    authentication_classes = []          # 🔥 REQUIRED (prevents 401)
    permission_classes = [AllowAny]       # 🔥 Public endpoint

    def post(self, request):
        email = request.data.get("email")

        # 1️⃣ Validate email
        if not email or not email.strip():
            return Response({"error": "Email is required"}, status=400)

        email = email.strip().lower()

        # 2️⃣ User must exist
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "Email not registered"}, status=404)

        # 3️⃣ User must be approved (ALL roles)
        if not user.is_approved:
            return Response(
                {"error": "Your email is not approved. Please contact admin."},
                status=403
            )

        # 4️⃣ Generate OTP
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
        user.save(update_fields=["otp", "otp_expires_at"])

        # 5️⃣ Send email (DEV-SAFE)
        try:
            send_mail(
                subject="KCET Login OTP",
                message=f"Your OTP is {otp}",
                from_email="kcetcompanion@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print("EMAIL ERROR:", e)
            return Response({"error": "Failed to send OTP"}, status=500)

        # ✅ DEV DEBUG
        print(f"🔐 OTP for {email}: {otp}")

        return Response({"message": "OTP sent successfully"}, status=200)
