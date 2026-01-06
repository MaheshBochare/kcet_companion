from rest_framework.viewsets import ModelViewSet
from core.models import ChatLog
from core.api.serializers import ChatLogSerializer

class ChatLogViewSet(ModelViewSet):
    queryset = ChatLog.objects.all().order_by("-timestamp")
    serializer_class = ChatLogSerializer
