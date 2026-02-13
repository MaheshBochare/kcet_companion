from core.infrastructure.repositories import SubscriberRepository
from core.services.utils.email_sender import EmailService
from django.conf import settings

class SubscriptionService:

    def subscribe(self, email):
        subscriber, created = SubscriberRepository.get_or_create(email)

        EmailService.send(
            "KCET Companion – Subscription Received",
            "Thank you for subscribing. Your request is under review.",
            email
        )

        if created:
            EmailService.send(
                "New Subscription Approval Needed",
                f"New subscriber: {email}",
                settings.ADMIN_EMAIL
            )

        return {
            "subscriber": subscriber,
            "created": created
        }
