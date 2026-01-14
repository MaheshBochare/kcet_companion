from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class CutoffRanksViewSet(ViewSet):
    """
    Builds the cutoff analyzer dataset:

    college_Namess | College_code | branchss | R_CATEGORY_ROUNDYEAR...
    Missing values are filled with 0.
    """

    def list(self, request):
        sql = """
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
        """

        # ------------------------------
        # Step 1: Execute SQL
        # ------------------------------
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        flat_data = [dict(zip(columns, row)) for row in rows]

        # ------------------------------
        # Step 2: Build matrix
        # ------------------------------
        all_cutoff_cols = set()
        result = {}

        for row in flat_data:
            key = f"{row['college_code']}_{row['branch']}"

            if key not in result:
                result[key] = {
                    "college_Namess": row["college"],
                    "College_code": row["college_code"],
                    "branchss": row["branch"]
                }

            cutoff_col = f"R_{row['category']}_{row['round']}{str(row['year'])[-2:]}"
            result[key][cutoff_col] = row["rank"]
            all_cutoff_cols.add(cutoff_col)

        # ------------------------------
        # Step 3: Fill missing values
        # ------------------------------
        for row in result.values():
            for col in all_cutoff_cols:
                if col not in row:
                    row[col] = 0

        return Response(list(result.values()))
