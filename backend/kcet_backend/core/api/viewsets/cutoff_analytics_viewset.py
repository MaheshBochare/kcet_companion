from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.cache import cache
from core.models import Cutoff, CollegeBranch


class CutoffAnalyticsViewSet(ViewSet):

    def list(self, request):
        colleges = request.query_params.getlist("college")
        branch = request.query_params.get("branch")

        categories = request.query_params.getlist("category")
        rounds = request.query_params.getlist("round")
        years = request.query_params.getlist("year")

        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        cache_key = f"cutoff_analytics:{request.get_full_path()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        # Base query
        cutoff_qs = Cutoff.objects.select_related(
            "college_branch", "college_branch__college", "college_branch__branch"
        )

        # Apply filters dynamically
        if colleges:
            cutoff_qs = cutoff_qs.filter(college_branch__college__College_name__in=colleges)

        if branch:
            cutoff_qs = cutoff_qs.filter(branch__Branch_Name__icontains=branch)

        if categories:
            cutoff_qs = cutoff_qs.filter(category__in=categories)

        if rounds:
            cutoff_qs = cutoff_qs.filter(round__in=rounds)

        if years:
            cutoff_qs = cutoff_qs.filter(year__in=years)

        combos = cutoff_qs.values("category", "round", "year").distinct()

        columns = ["college", "branch"] + [
            f"{c['category']}_{c['round']}_{c['year']}" for c in combos
        ]

        unique_pairs = cutoff_qs.values(
            "college_branch__college__College_name",
            "college_branch__branch__Branch_Name"
        ).distinct()

        total = len(unique_pairs)
        start = (page - 1) * page_size
        end = start + page_size
        pairs = unique_pairs[start:end]

        rows = []

        for p in pairs:
            row = {
                "college": p["college_branch__college__College_name"],
                "branch": p["college_branch__branch__Branch_Name"]
            }

            for c in combos:
                col = f"{c['category']}_{c['round']}_{c['year']}"
                row[col] = None

                match = cutoff_qs.filter(
                    college_branch__college__College_name=p["college_branch__college__College_name"],
                    college_branch__branch__Branch_Name=p["college_branch__branch__Branch_Name"],
                    category=c["category"],
                    round=c["round"],
                    year=c["year"]
                ).first()

                if match:
                    row[col] = match.rank

            rows.append(row)

        result = {
            "page": page,
            "page_size": page_size,
            "total_rows": total,
            "columns": columns,
            "rows": rows
        }

        cache.set(cache_key, result, timeout=60 * 30)

        return Response(result)
