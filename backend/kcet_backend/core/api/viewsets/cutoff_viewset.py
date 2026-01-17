from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response as DRFResponse

from core.models import Cutoff
from core.api.serializers import CutoffSerializer
from core.utils.cache_utils import get_or_set_cache
from core.utils.json_safe import make_json_safe
class CutoffViewSet(ModelViewSet):
    queryset = Cutoff.objects.select_related(
        "college_branch", "year", "category", "round"
    ).all()
    serializer_class = CutoffSerializer

    def list(self, request, *args, **kwargs):
        """
        GET /api/cutoffs/
        Redis cached (no pagination)
        """

        def compute():
            serializer = self.get_serializer(self.get_queryset(), many=True)
            data = serializer.data

            for row in data:
                for key, value in row.items():
                    row[key] = make_json_safe(value)

            return data

        data = get_or_set_cache(
            key="cutoff_list_all",   # single Redis key
            ttl=60 * 10,             # 10 minutes
            compute_func=compute
        )

        return DRFResponse(data)
