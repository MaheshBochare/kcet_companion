import numpy as np
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import models

from core.models import College, CollegeBranch, SeatMatrix, Cutoff


MAX_RANK = 130000


# =================== DATA CLEANING ===================

def clean_data(values):
    values = [v for v in values if v is not None and 0 < v <= MAX_RANK]

    if len(values) < 10:
        return np.array(values)

    values = np.array(values)

    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1

    low = q1 - 1.2 * iqr
    high = q3 + 1.2 * iqr

    return values[(values >= low) & (values <= high)]


# =================== VIEWSET ===================

class KeyStatisticsViewSet(ViewSet):

    @method_decorator(cache_page(60 * 15))
    def list(self, request):

        # ---------- BASIC COUNTS ----------
        total_colleges = College.objects.count()

        top_rated = College.objects.filter(naaccrating__in=["A+", "A++"]).count()

        locations = (
            College.objects.exclude(location__isnull=True)
            .exclude(location__exact="")
            .values("location").distinct().count()
        )

        branches = CollegeBranch.objects.values("branch").distinct().count()

        # ---------- CLEANED CUTOFF STATS ----------
        raw_ranks = list(Cutoff.objects.values_list("rank", flat=True))
        clean_ranks = clean_data(raw_ranks)

        if len(clean_ranks) == 0:
            avg_rank = min_rank = max_rank = median_rank = std_rank = 0
        else:
            avg_rank = int(np.mean(clean_ranks))
            min_rank = int(np.min(clean_ranks))
            max_rank = int(np.max(clean_ranks))
            median_rank = int(np.median(clean_ranks))
            std_rank = float(np.std(clean_ranks))

        # ---------- CLEANED SEAT STATS ----------
        raw_seats = list(SeatMatrix.objects.values_list("total_seats", flat=True))
        clean_seats = clean_data(raw_seats)
        total_seats = int(np.sum(clean_seats)) if len(clean_seats) else 0

        total_capacity = SeatMatrix.objects.aggregate(total=models.Sum("total_seats"))["total"] or 0
        total_filled = SeatMatrix.objects.aggregate(total=models.Sum("filled_seats"))["total"] or 0
        seat_utilization = round((total_filled / total_capacity) * 100, 2) if total_capacity else 0

        # ---------- YEARLY TREND ----------
        yearly = []
        for year in Cutoff.objects.values_list("year", flat=True).distinct():
            yr = list(Cutoff.objects.filter(year=year).values_list("rank", flat=True))
            yr_clean = clean_data(yr)
            if len(yr_clean):
                yearly.append({"year": year, "avg_rank": int(np.mean(yr_clean))})

        # ---------- CATEGORY ANALYTICS ----------
        category_stats = []
        for cat in Cutoff.objects.values_list("category", flat=True).distinct():
            r = list(Cutoff.objects.filter(category=cat).values_list("rank", flat=True))
            c = clean_data(r)
            if len(c):
                category_stats.append({
                    "category": cat,
                    "avg_rank": int(np.mean(c)),
                    "min_rank": int(np.min(c)),
                    "max_rank": int(np.max(c))
                })

        # ---------- BRANCH ANALYTICS ----------
        branch_stats = []
        for br in CollegeBranch.objects.values_list("branch__Branch_Name", flat=True).distinct():
            r = list(Cutoff.objects.filter(college_branch__branch__Branch_Name=br).values_list("rank", flat=True))
            c = clean_data(r)
            if len(c):
                branch_stats.append({
                    "branch": br,
                    "avg_rank": int(np.mean(c)),
                    "min_rank": int(np.min(c)),
                    "max_rank": int(np.max(c))
                })

        # ---------- ADVANCED METRICS ----------
        branch_comp = {b["branch"]: b["avg_rank"] for b in branch_stats}

        most_competitive_branch = min(branch_comp, key=branch_comp.get) if branch_comp else "N/A"
        least_competitive_branch = max(branch_comp, key=branch_comp.get) if branch_comp else "N/A"

        category_popularity = {
            c: Cutoff.objects.filter(category=c).count()
            for c in Cutoff.objects.values_list("category", flat=True).distinct()
        }

        most_popular_category = max(category_popularity, key=category_popularity.get) if category_popularity else "N/A"

        competition_intensity = round(100000 / (avg_rank + 1), 3) if avg_rank else 0
        rank_volatility = round(std_rank / (avg_rank + 1), 4) if avg_rank else 0

        # ---------- CONFIDENCE INTERVAL ----------
        lower = int(max(avg_rank - 1.96 * std_rank, 0)) if avg_rank else 0
        upper = int(avg_rank + 1.96 * std_rank) if avg_rank else 0

        return Response({
            "overview": [
                {"name": "Total Colleges", "value": total_colleges},
                {"name": "Top Rated Colleges", "value": top_rated},
                {"name": "Locations", "value": locations},
                {"name": "Branches Offered", "value": branches},
                {"name": "Total Seats", "value": total_seats},
                {"name": "Avg Cutoff Rank", "value": avg_rank},
                {"name": "Median Cutoff Rank", "value": median_rank},
                {"name": "Min Cutoff Rank", "value": min_rank},
                {"name": "Max Cutoff Rank", "value": max_rank},
            ],

            "trends": {
                "yearly": yearly,
                "category": category_stats,
                "branch": branch_stats
            },

            "advanced_stats": {
                "seat_utilization_percent": seat_utilization,
                "most_competitive_branch": most_competitive_branch,
                "least_competitive_branch": least_competitive_branch,
                "most_popular_category": most_popular_category,
                "competition_intensity_score": competition_intensity,
                "rank_volatility_index": rank_volatility
            },

            "prediction": {
                "confidence_interval": [lower, upper]
            }
        })
