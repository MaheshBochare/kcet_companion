from rest_framework.viewsets import ModelViewSet
from core.models import SeatMatrix
from core.api.serializers import SeatMatrixSerializer

class SeatMatrixViewSet(ModelViewSet):
    queryset = SeatMatrix.objects.select_related(
        "college_branch", "year", "category", "round"
    ).all()
    serializer_class = SeatMatrixSerializer
