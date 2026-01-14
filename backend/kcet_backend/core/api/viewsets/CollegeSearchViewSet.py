from django.db.models import Count, FloatField, F
from django.db.models.functions import Cast

# inside list()

qs = (
    College.objects
    .annotate(
        rank=Coalesce(SearchRank(SearchVector("College_name"), q), Value(0.0)),
        similarity=Coalesce(TrigramSimilarity("College_name", q), Value(0.0)),
        popularity=Count("college_branches__cutoff"),
    )
    .annotate(
        final_score=F("rank") * 0.6 + F("similarity") * 0.3 + Cast(F("popularity"), FloatField()) * 0.1
    )
    .filter(similarity__gt=0.1)
    .order_by("-final_score")
)[:10]
