from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import CutoffRank

class CutoffView(APIView):
    def get(self, request):
        college = request.GET.get("college")
        branch = request.GET.get("branch")

        qs = CutoffRank.objects.all()
        if college:
            qs = qs.filter(college__college_code=college)
        if branch:
            qs = qs.filter(branch__branch_name__icontains=branch)

        return Response(list(qs.values()))
