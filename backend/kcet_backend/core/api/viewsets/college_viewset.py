from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from core.models import College
from core.api.serializers import CollegeSerializer
from core.utils.json_safe import make_json_safe
from core.utils.cache_utils import get_or_set_cache
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class CollegeViewSet(ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = serializer.data

        for row in data:
            for key, value in row.items():
                row[key] = make_json_safe(value)

        return Response(data)
        data = get_or_set_cache(
            key="colleges_list",     # Redis key
            ttl=60 * 5,              # 5 minutes
            compute_func=compute
        )
        return Response(data)
