from core.models import Subscriber

class SubscriberRepository:
    @staticmethod
    def get_or_create(email):
        return Subscriber.objects.get_or_create(email=email)
