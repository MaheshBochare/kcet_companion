import math
from django.core.cache import cache
from django.db.models import F, Value, FloatField
from django.db.models.functions import Coalesce
from django.contrib.postgres.search import SearchVector, SearchRank, TrigramSimilarity
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from core.models import College


# ---------- Safe Serialization ----------
def safe_number(x):
    if x is None:
        return None
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    return x


class CollegeSearchViewSet(ViewSet):

    def list(self, request):
        query = request.query_params.get("q", "").strip().lower()

        if len(query) < 2:
            return Response({"results": []})

        # ---------- Cache ----------
        cache_key = f"college_search:{query}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        # ---------- Search Logic ----------
        qs = (
            College.objects
            .annotate(
                rank=Coalesce(
                    SearchRank(SearchVector("College_name"), query),
                    Value(0.0),
                    output_field=FloatField()
                ),
                similarity=Coalesce(
                    TrigramSimilarity("College_name", query),
                    Value(0.0),
                    output_field=FloatField()
                ),
                popularity=Coalesce(F("highestpackage"), Value(0), output_field=FloatField()),
                relevance=F("rank") * 0.6 + F("similarity") * 0.4,
                final_score=F("relevance") * 0.7 + F("popularity") * 0.3
            )
            .filter(similarity__gt=0.15)
            .order_by("-final_score")[:12]
        )

        results = []
        for c in qs:
            fees = safe_number(c.firstyearfees)
            if fees is None:
                fees = 450000   # your default

            rating = c.naaccrating
            if not rating:
                rating = 3.5    # your default

            results.append({
                "name": c.College_name,
                "location": c.location,
                "naac": rating,
                "fees": fees,
                "highest_package": safe_number(c.highestpackage),
                "score": safe_number(c.final_score),
            })

        payload = {"results": results}

        # Cache for 10 minutes
        cache.set(cache_key, payload, 600)

        return Response(payload)
