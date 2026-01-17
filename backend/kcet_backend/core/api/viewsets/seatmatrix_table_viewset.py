from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.cache import cache

from core.utils.cache_utils import make_cache_key


class SeatMatrixTableViewSet(ViewSet):
    """
    Seat Matrix Analyzer Table API
    - College + Branch level
    - Category + Round + Year pivot
    - Cached + Paginated
    """

    PAGE_SIZE = 25
    CACHE_TTL = 60 * 30  # 30 minutes

    def list(self, request):
        # ------------------------------
        # Query params
        # ------------------------------
        page = int(request.query_params.get("page", 1))
        college_code = request.query_params.get("college")
        branch_name = request.query_params.get("branch")
        year = request.query_params.get("year")
        category = request.query_params.get("category")
        round_code = request.query_params.get("round")

        cache_key = make_cache_key(
            "seatmatrix_table",
            page,
            college_code or "ALL",
            branch_name or "ALL",
            year or "ALL",
            category or "ALL",
            round_code or "ALL",
        )

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        # ------------------------------
        # WHERE clause
        # ------------------------------
        where = []
        params = []

        if college_code:
            where.append('c."college_code" = %s')
            params.append(college_code)

        if branch_name:
            where.append('b."Branch_Name" = %s')
            params.append(branch_name)

        if year:
            where.append("y.year_code = %s")
            params.append(year)

        if category:
            where.append("ca.category_code = %s")
            params.append(category)

        if round_code:
            where.append("r.round_code = %s")
            params.append(round_code)

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""

        # ------------------------------
        # SQL
        # ------------------------------
        sql = f"""
        SELECT
            c."College_name" AS college,
            c."college_code" AS college_code,
            b."Branch_Name"  AS branch,

            ca.category_code AS category,
            r.round_code     AS round,
            y.year_code      AS year,

            sm.total_seats,
            sm.filled_seats,
            sm.available_seats

        FROM seat_matrix sm
        JOIN category ca ON sm.category_id = ca.id
        JOIN round r     ON sm.round_id = r.id
        JOIN year_dim y  ON sm.year_id = y.id

        JOIN college_branch cb ON sm.college_branch_id = cb.id
        JOIN core_college c    ON cb."college_code" = c."college_code"
        JOIN core_branch b     ON cb."Branch_Code" = b."Branch_Code"

        {where_sql}
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()

        flat = [dict(zip(cols, r)) for r in rows]

        # ------------------------------
        # Build matrix
        # ------------------------------
        matrix = {}
        all_cols = set()

        for r in flat:
            key = f"{r['college_code']}_{r['branch']}"

            if key not in matrix:
                matrix[key] = {
                    "college_name": r["college"],
                    "college_code": r["college_code"],
                    "branch": r["branch"],
                }

            col_prefix = f"S_{r['category']}_{r['round']}{str(r['year'])[-2:]}"

            matrix[key][f"{col_prefix}_total"] = r["total_seats"]
            matrix[key][f"{col_prefix}_filled"] = r["filled_seats"]
            matrix[key][f"{col_prefix}_available"] = r["available_seats"]

            all_cols.update([
                f"{col_prefix}_total",
                f"{col_prefix}_filled",
                f"{col_prefix}_available",
            ])

        # ------------------------------
        # Fill missing columns
        # ------------------------------
        result = []
        for row in matrix.values():
            for c in all_cols:
                row.setdefault(c, 0)
            result.append(row)

        # ------------------------------
        # Pagination
        # ------------------------------
        paginator = Paginator(result, self.PAGE_SIZE)
        page_obj = paginator.get_page(page)

        response = {
            "filters": {
                "college": college_code,
                "branch": branch_name,
                "year": year,
                "category": category,
                "round": round_code,
            },
            "pagination": {
                "current_page": page,
                "total_pages": paginator.num_pages,
                "total_records": paginator.count,
                "page_size": self.PAGE_SIZE,
            },
            "results": list(page_obj.object_list),
        }

        cache.set(cache_key, response, self.CACHE_TTL)
        return Response(response)
