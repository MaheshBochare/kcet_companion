from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import SeatMatrix

class SeatMatrixView(APIView):
    def get(self, request):
        college = request.GET.get("college")
        qs = SeatMatrix.objects.all()

        if college:
            qs = qs.filter(college_branch__college__college_code=college)

        return Response(list(qs.values()))
