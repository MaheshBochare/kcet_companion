from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.cache import cache
from core.models import College
from core.api.serializers import FeaturedCollegeSerializer
import math
import random


class FeaturedCollegeViewSet(ViewSet):

    CACHE_KEY = "featured_colleges"
    CACHE_TTL = 30   # seconds

    def list(self, request):
        # 🔁 Try cache first
        cached = cache.get(self.CACHE_KEY)
        if cached:
            return Response(cached)

        # ----------------------------
        # Fetch & rotate colleges
        # ----------------------------
        colleges = list(
            College.objects.only(
                "college_code",
                "College_name",
                "location",
                "highestpackage",
                "naaccrating"
            )
        )

        random.shuffle(colleges)
        colleges = colleges[:6]

        raw = []

        for c in colleges:
            hp = c.highestpackage

            # Sanitize numeric fields
            if hp is None or (isinstance(hp, float) and math.isnan(hp)):
                hp = 0.0

            raw.append({
                "college_code": c.college_code,
                "name": c.College_name,
                "location": c.location,
                "naac": c.naaccrating,
                "highest_package": hp,
            })

        serializer = FeaturedCollegeSerializer(raw, many=True)

        response_data = {
            "featured_colleges": serializer.data
        }

        # 🔐 Store in cache
        cache.set(self.CACHE_KEY, response_data, timeout=self.CACHE_TTL)

        return Response(response_data)
