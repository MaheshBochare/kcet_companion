from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import College, CutoffRank, SeatMatrix

class StatsView(APIView):
    def get(self, request):
        return Response({
            "colleges": College.objects.count(),
            "cutoff_records": CutoffRank.objects.count(),
            "seat_records": SeatMatrix.objects.count(),
        })

