from django.shortcuts import render 
import os, tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.services.preprocessing.seat_matrix import SeatMatrixIngestionService
import random

from django.http import JsonResponse
from core.tasks import scrape_and_ingest_colleges

def refresh_colleges(request):
    task = scrape_and_ingest_colleges.delay()
    return JsonResponse({
        "message": "Scraping started",
        "task_id": task.id
    })


import os, tempfile
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.services.preprocessing.seat_matrix import SeatMatrixIngestionService

@csrf_exempt
def upload_seatmatrix(request):

    # Show upload form
    if request.method == "GET":
        return render(request, "upload_seatmatrix.html")

    # Handle upload
    pdf = request.FILES.get("pdf")
    year = request.POST.get("year")
    round_code = request.POST.get("round")

    if not pdf or not year or not round_code:
        return JsonResponse({"error": "Missing file, year or round"}, status=400)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        for chunk in pdf.chunks():
            temp.write(chunk)
        temp_path = temp.name

    try:
        SeatMatrixIngestionService.ingest(temp_path, year, round_code)
    finally:
        os.remove(temp_path)

    return JsonResponse({"status": "success", "message": "Seat matrix ingested successfully"})

import random
from core.models import College

FEATURE_TYPES = ["TOP_RATED", "BEST_ROI", "PREMIUM", "EMERGING"]

def home_view(request):

    feature_type = random.choice(FEATURE_TYPES)

    if feature_type == "TOP_RATED":
        qs = College.objects.filter(Rating__gte=4.5).order_by("-Rating")

    elif feature_type == "BEST_ROI":
        qs = College.objects.filter(averagepackage__gte=8).order_by("-averagepackage")

    elif feature_type == "PREMIUM":
        qs = College.objects.filter(firstyearfees__gte=150000).order_by("-Rating")

    else:
        qs = College.objects.filter(Rating__gte=3.5, Rating__lt=4.5).order_by("-Rating")


    colleges = list(qs[:5])  # top 5 of that category
    featured_sample = random.sample(colleges, min(3, len(colleges)))

    featured_colleges = []
    for c in featured_sample:
        featured_colleges.append({
            "id": c.college_code,
            "name": c.College_name,
            "description": f"{c.location} • NAAC {c.approvals} • Avg ₹{c.averagepackage} LPA",
            "badge": feature_type.replace("_", " ").title()
        })

    return render(request, "home/index.html", {
        "featured_colleges": featured_colleges,
        "feature_title": feature_type.replace("_", " ").title(),
        "statistics": [
            {"name": "Total Colleges", "value": College.objects.count()},
            {"name": "Top Rated", "value": College.objects.filter(Rating__gte=4.5).count()},
            {"name": "Locations", "value": College.objects.values("location").distinct().count()},
        ],
        "quick_links": [
            {"title": "Cutoff Analyzer", "url": "/home/cutoff_analyzer"},
            {"title": "Seat Matrix", "url": "/home/seat_matrix"},
            {"title": "Admission Predictor", "url": "/home/predictor"},
            {"title": "Analytics Dashboard", "url": "/home/dashboard"},
        ]
    })



from django.http import JsonResponse
from django.db.models import Q

def search_suggestions(request):
    q = request.GET.get("q", "")
    results = College.objects.filter(
        Q(College_name__icontains=q) |
        Q(location__icontains=q)
    )[:8]

    data = []
    for c in results:
        data.append({
            "college": c.College_name,
            "location": c.location,
            "affiliation": c.approvals,
            "cutoff": getattr(c, "latest_cutoff", None),
            "fees": c.firstyearfees
        })

    return JsonResponse({"suggestions": data})
import uuid
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from core.infrastructure.django_models.roles import User
from core.utils.otplogic import set_otp

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        set_otp(user)
        return Response({"message": "OTP sent"})

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        user = User.objects.filter(email=email, otp=otp).first()
        if not user or user.otp_expiry < timezone.now():
            return Response({"error": "Invalid OTP"}, status=400)

        session_id = uuid.uuid4()
        user.current_session_id = session_id
        user.otp = None
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh["session_id"] = str(session_id)

        response = Response({"role": user.role})

        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            samesite="Lax",
        )

        response.set_cookie(
            "session_id",
            str(session_id),
            httponly=False,
        )

        return response
