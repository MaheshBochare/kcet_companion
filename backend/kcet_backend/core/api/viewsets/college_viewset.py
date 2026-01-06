from rest_framework.viewsets import ModelViewSet
from core.models import College
from core.api.serializers import CollegeSerializer

class CollegeViewSet(ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
