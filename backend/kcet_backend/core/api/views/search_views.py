from rapidfuzz import process, fuzz
from django.http import JsonResponse
from core.models import College

def search_suggestions(request):
    q = request.GET.get("q","").lower()
    colleges = list(College.objects.values("college_name","location","college_code"))

    names = [c["college_name"] for c in colleges]
    matches = process.extract(q, names, scorer=fuzz.WRatio, limit=10)

    results = []
    for name, score, idx in matches:
        if score >= 60:
            results.append({**colleges[idx], "score": score})

    return JsonResponse({"suggestions": results})
