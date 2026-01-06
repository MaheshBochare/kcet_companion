from rest_framework.viewsets import ModelViewSet
from core.models import Cutoff
from core.api.serializers import CutoffSerializer

class CutoffViewSet(ModelViewSet):
    queryset = Cutoff.objects.select_related(
        "college_branch", "year", "category", "round"
    ).all()
    serializer_class = CutoffSerializer
