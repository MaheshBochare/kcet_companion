from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response as DRFResponse
from django.core.paginator import Paginator

from core.utils.cache_utils import get_or_set_cache, make_cache_key
class CutoffRanksViewSet(ViewSet):
    """
    Cutoff analyzer matrix API
    - Filterable by college, branch, category, round, year
    - Redis cached
    - Paginated
    """

    PAGE_SIZE = 25

    def list(self, request):
        # ------------------------------
        # Read query params
        # ------------------------------
        page = int(request.query_params.get("page", 1))

        college_code = request.query_params.get("college")    # E021
        branch_name  = request.query_params.get("branch")     # CSE
        category     = request.query_params.get("category")   # GM
        round_code   = request.query_params.get("round")      # 1 / 2
        year         = request.query_params.get("year")       # 2024

        # ------------------------------
        # Cache key (FULLY filter-aware)
        # ------------------------------
        cache_key = make_cache_key(
            "cutoff_ranks_matrix",
            page,
            college_code or "ALL",
            branch_name or "ALL",
            category or "ALL",
            round_code or "ALL",
            year or "ALL",
        )

        def compute():
            # ------------------------------
            # Build WHERE clause safely
            # ------------------------------
            where_clauses = []
            params = []

            if college_code:
                where_clauses.append('c."college_code" = %s')
                params.append(college_code)

            if branch_name:
                where_clauses.append('b."Branch_Name" = %s')
                params.append(branch_name)

            if category:
                where_clauses.append("ca.category_code = %s")
                params.append(category)

            if round_code:
                where_clauses.append("r.round_code = %s")
                params.append(round_code)

            if year:
                where_clauses.append("y.year_code = %s")
                params.append(year)

            where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            # ------------------------------
            # SQL Query
            # ------------------------------
            sql = f"""
            SELECT
                c."College_name"   AS college,
                c."college_code"   AS college_code,
                b."Branch_Name"    AS branch,
                ca.category_code   AS category,
                r.round_code       AS round,
                y.year_code        AS year,
                co.rank            AS rank
            FROM core_cutoff co
            JOIN category ca ON co.category_id = ca.id
            JOIN round r     ON co.round_id = r.id
            JOIN year_dim y  ON co.year_id = y.id
            JOIN college_branch cb ON co.college_branch_id = cb.id
            JOIN core_college c    ON cb."college_code" = c."college_code"
            JOIN core_branch b     ON cb."Branch_Code" = b."Branch_Code"
            {where_sql}
            """

            # ------------------------------
            # Execute SQL
            # ------------------------------
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            flat_data = [dict(zip(columns, row)) for row in rows]

            # ------------------------------
            # Build cutoff matrix
            # ------------------------------
            all_cutoff_cols = set()
            matrix = {}

            for row in flat_data:
                key = f"{row['college_code']}_{row['branch']}"

                if key not in matrix:
                    matrix[key] = {
                        "college_name": row["college"],
                        "college_code": row["college_code"],
                        "branch": row["branch"],
                    }

                cutoff_col = f"R_{row['category']}_{row['round']}{str(row['year'])[-2:]}"
                matrix[key][cutoff_col] = row["rank"]
                all_cutoff_cols.add(cutoff_col)

            # ------------------------------
            # Fill missing values with 0
            # ------------------------------
            rows_list = []
            for r in matrix.values():
                for col in all_cutoff_cols:
                    r.setdefault(col, 0)
                rows_list.append(r)

            # ------------------------------
            # Pagination
            # ------------------------------
            paginator = Paginator(rows_list, self.PAGE_SIZE)
            page_obj = paginator.get_page(page)

            return {
                "filters": {
                    "college": college_code,
                    "branch": branch_name,
                    "category": category,
                    "round": round_code,
                    "year": year,
                },
                "pagination": {
                    "current_page": page,
                    "total_pages": paginator.num_pages,
                    "total_records": paginator.count,
                    "page_size": self.PAGE_SIZE,
                },
                "results": list(page_obj.object_list),
            }

        # ------------------------------
        # Redis get-or-set
        # ------------------------------
        data = get_or_set_cache(
            key=cache_key,
            ttl=60 * 30,   # 30 minutes
            compute_func=compute
        )

        return DRFResponse(data)
