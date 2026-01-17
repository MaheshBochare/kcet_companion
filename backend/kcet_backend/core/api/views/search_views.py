from django.http import JsonResponse
from core.models import College


def search_colleges(request):
    q = request.GET.get("q", "").strip()

    results = College.objects.filter(College_name__icontains=q)[:10]

    data = [{
        "name": c.College_name,
        "location": c.location,
        "naac": c.naaccrating,
        "fees": c.firstyearfees,
        "highest_package": c.highestpackage
    } for c in results]

    return JsonResponse({"results": data})
