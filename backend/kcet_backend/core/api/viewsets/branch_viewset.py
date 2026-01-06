from rest_framework.viewsets import ModelViewSet
from core.models import Branch
from core.api.serializers import BranchSerializer


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
