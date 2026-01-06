from django.core.mail import send_mail
from django.conf import settings

class EmailService:
    @staticmethod
    def send(subject, message, recipient):
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
