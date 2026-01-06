from rest_framework.viewsets import ModelViewSet
from core.models import Subscriber
from core.api.serializers import SubscriberSerializer

class SubscriberViewSet(ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
