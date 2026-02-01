from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ======================
# ViewSets
# ======================
#from backend.kcet_backend.core.api.views.ResendOTP import ResendOTPView
from core.api.views.ResendOTP import ResendOTPView
from core.api.views.Logout_view import LogoutView
from core.api.viewsets.college_viewset import CollegeViewSet
from core.api.viewsets.branch_viewset import BranchViewSet
from core.api.viewsets.cutoff_viewset import CutoffViewSet
from core.api.viewsets.seat_matrix_viewset import SeatMatrixViewSet
from core.api.viewsets.Category_viewset import CategoryViewSet
from core.api.viewsets.subscriber_viewset import SubscriberViewSet
from core.api.viewsets.chatlog_viewset import ChatLogViewSet
from core.api.viewsets.search_viewset import CollegeSearchViewSet
from core.api.viewsets.seatmatrix_table_viewset import SeatMatrixTableViewSet
from core.api.viewsets.featured_college_viewset import FeaturedCollegeViewSet
from core.api.viewsets.key_statistics_viewset import KeyStatisticsViewSet
from core.api.viewsets.quick_links_viewset import QuickLinksViewSet
from core.api.viewsets.cutoff_analytics_viewset import CutoffAnalyticsViewSet
from core.api.viewsets.seatmatrix_analytics_viewset import SeatMatrixAnalyticsViewSet
from core.api.viewsets.cutoff_table_viewsets import CutoffRanksViewSet
from rest_framework_simplejwt.views import TokenRefreshView



# ======================
# API Views (Auth / Roles)
# ======================
from core.api.views.auth_otp import SendOTPView
from core.api.views.auth_login import VerifyOTPView
from core.api.views.auth_test import AuthTestView
from core.api.views.csrf import csrf_token_view
from core.api.views.user_views import UserHomeView
from core.api.views.admin_views import SystemSettingsView, ApprovedGmailView

# ======================
# Router
# ======================
router = DefaultRouter()
router.register("colleges", CollegeViewSet)
router.register("branches", BranchViewSet)
router.register("cutoffs", CutoffViewSet)
router.register("seatmatrix", SeatMatrixViewSet)
router.register("categories", CategoryViewSet)
router.register("subscribers", SubscriberViewSet)
router.register("chatlogs", ChatLogViewSet)
router.register("featured-colleges", FeaturedCollegeViewSet, basename="featured-colleges")
router.register("key-statistics", KeyStatisticsViewSet, basename="key-statistics")
router.register("quick-links", QuickLinksViewSet, basename="quick-links")
router.register("search", CollegeSearchViewSet, basename="search")
router.register("cutoff-analytics", CutoffAnalyticsViewSet, basename="cutoff-analytics")
router.register("seatmatrix-analytics", SeatMatrixAnalyticsViewSet, basename="seatmatrix-analytics")
router.register("cutoff-table", CutoffRanksViewSet, basename="cutoff-table")
router.register("seatmatrix-table", SeatMatrixTableViewSet, basename="seatmatrix-table")

# ======================
# URL Patterns
# ======================
urlpatterns = [
    # Router URLs
    path("", include(router.urls)),

    # CSRF
    path("csrf/", csrf_token_view),

    # Auth
    path("auth/send-otp/", SendOTPView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("auth/auth-test/", AuthTestView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Owner
    path("owner/system/", SystemSettingsView.as_view()),

    # Admin
    path("admin/approve-gmail/", ApprovedGmailView.as_view()),

    # User
    path("user/home/", UserHomeView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/resend-otp/", ResendOTPView.as_view()),


]
