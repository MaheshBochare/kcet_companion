from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from core.models import College
from core.api.serializers import FeaturedCollegeSerializer
import math


class FeaturedCollegeViewSet(ViewSet):

    def list(self, request):
        colleges = (
            College.objects
            .only("College_name", "location", "highestpackage", "naaccrating")
            .order_by("-naaccrating", "-highestpackage")[:6]
        )

        raw = []

        for c in colleges:
            hp = c.highestpackage

            # 🔥 CRITICAL FIX — sanitize BEFORE JSON serialization
            if hp is None or (isinstance(hp, float) and math.isnan(hp)):
                hp = 0.0

            raw.append({
                "name": c.College_name,
                "location": c.location,
                "naac": c.naaccrating,
                "highest_package": hp,
            })

        serializer = FeaturedCollegeSerializer(raw, many=True)

        return Response({
            "featured_colleges": serializer.data
        })
