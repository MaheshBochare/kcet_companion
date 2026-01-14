from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from core.models import College


@cache_page(60 * 30)  # Cache for 30 minutes
def featured_colleges(request):
    colleges = (
        College.objects
        .only("College_name", "location", "highestpackage", "naaccrating")
        .order_by("-naaccrating", "-highestpackage")[:6]
    )

    result = []
    for c in colleges:
        result.append({
            "name": c.College_name,
            "location": c.location,
            "naac": c.naaccrating,
            "highest_package": c.highestpackage,
        })

    return JsonResponse({"featured_colleges": result})
