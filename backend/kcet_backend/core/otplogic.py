import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def set_otp(user):
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = timezone.now() + timedelta(minutes=5)
    user.save()

    send_mail(
        "Your Login OTP",
        f"Your OTP is {otp}",
        "noreply@kcet.com",
        [user.email],
    )
