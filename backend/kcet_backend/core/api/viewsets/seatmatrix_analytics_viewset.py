from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.cache import cache
from core.models import SeatMatrix


# ===================== CODE MAPPINGS =====================

CATEGORY_MAP = {
    1: "GM",
    2: "2AG",
    3: "2BG",
    4: "3AG",
    5: "3BG",
    6: "SC",
    7: "ST",
}

ROUND_MAP = {
    1: "1GEN",
    2: "2GEN",
    3: "2EXTGEN",
    4: "SPECIAL",
    5: "FINAL",
}

YEAR_MAP = {
    1: "21",
    2: "22",
    3: "23",
    4: "24",
    5: "25",
}


class SeatMatrixAnalyticsViewSet(ViewSet):

    def list(self, request):

        colleges = request.query_params.getlist("college")
        branch = request.query_params.get("branch")
        categories = request.query_params.getlist("category")
        rounds = request.query_params.getlist("round")
        years = request.query_params.getlist("year")

        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        cache_key = f"seatmatrix_analytics:{request.get_full_path()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        qs = SeatMatrix.objects.select_related(
            "college_branch", "college_branch__college", "college_branch__branch"
        )

        # ===================== APPLY FILTERS =====================

        if colleges:
            qs = qs.filter(college_branch__college__College_name__in=colleges)

        if branch:
            qs = qs.filter(college_branch__branch__Branch_Name__icontains=branch)

        if categories:
            qs = qs.filter(category__in=categories)

        if rounds:
            qs = qs.filter(round__in=rounds)

        if years:
            qs = qs.filter(year__in=years)

        # ===================== BUILD DYNAMIC COLUMNS =====================

        combos = qs.values("category", "round", "year").distinct()

        columns = ["college", "branch"]

        for c in combos:
            cat = CATEGORY_MAP.get(c["category"], str(c["category"]))
            rnd = ROUND_MAP.get(c["round"], str(c["round"]))
            yr  = YEAR_MAP.get(c["year"], str(c["year"]))
            columns.append(f"{cat}_{rnd}_{yr}")

        # ===================== ROW GENERATION =====================

        unique_pairs = qs.values(
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
                cat = CATEGORY_MAP.get(c["category"], str(c["category"]))
                rnd = ROUND_MAP.get(c["round"], str(c["round"]))
                yr  = YEAR_MAP.get(c["year"], str(c["year"]))
                col = f"{cat}_{rnd}_{yr}"

                row[col] = {
                    "total": None,
                    "filled": None,
                    "available": None
                }

                match = qs.filter(
                    college_branch__college__College_name=row["college"],
                    college_branch__branch__Branch_Name=row["branch"],
                    category=c["category"],
                    round=c["round"],
                    year=c["year"]
                ).first()

                if match:
                    row[col] = {
                        "total": match.total_seats,
                        "filled": match.filled_seats,
                        "available": match.available_seats
                    }

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
