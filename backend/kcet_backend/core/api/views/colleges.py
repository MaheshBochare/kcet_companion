from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import College

class CollegeListView(APIView):
    def get(self, request):
        qs = College.objects.all().values(
            "college_code", "college_name", "location", "college_type"
        )
        return Response(list(qs))
