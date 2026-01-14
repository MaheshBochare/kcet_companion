from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from core.models import College
from core.api.serializers import CollegeSerializer
from core.utils.json_safe import make_json_safe


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
