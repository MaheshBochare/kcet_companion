from django.urls import path
from rest_framework.routers import DefaultRouter
from core.api.viewsets.college_viewset import CollegeViewSet
from core.api.viewsets.branch_viewset import BranchViewSet
from core.api.viewsets.cutoff_viewset import CutoffViewSet
from core.api.viewsets.seat_matrix_viewset import SeatMatrixViewSet
from core.api.viewsets.Category_viewset import CategoryViewSet
from core.api.viewsets.subscriber_viewset import SubscriberViewSet
from core.api.viewsets.chatlog_viewset import ChatLogViewSet
from core.api.viewsets.search_viewset import CollegeSearchViewSet 
#from core.api.views.chatbot_view import KCETChatbotView
'''from core.api.views.search_views import search_suggestions
from core.api.views.colleges import CollegeListView
from core.api.views.cutoff import CutoffView
from core.api.views.seatmatrix import SeatMatrixView
from core.api.views.stats import StatsView'''
#from core.api.views.cutoff import CutoffView
from django.urls import path
from . import views
from core.api.viewsets.featured_college_viewset import FeaturedCollegeViewSet
from core.api.viewsets.key_statistics_viewset import KeyStatisticsViewSet
from core.api.viewsets.quick_links_viewset import QuickLinksViewSet
from core.api.views.search_views import search_colleges
from core.api.viewsets.cutoff_analytics_viewset import CutoffAnalyticsViewSet
from core.api.viewsets.seatmatrix_analytics_viewset import SeatMatrixAnalyticsViewSet
from core.api.viewsets.cutoff_table_viewsets import CutoffRanksViewSet

router = DefaultRouter()
router.register("colleges", CollegeViewSet)
router.register("branches", BranchViewSet)
router.register("cutoffs", CutoffViewSet)
router.register("seatmatrix", SeatMatrixViewSet)
router.register("categories", CategoryViewSet)
router.register("subscribers", SubscriberViewSet)
router.register("chatlogs", ChatLogViewSet)
router.register("featured-colleges", FeaturedCollegeViewSet, basename="featured-colleges")
#router.register("chatbot", KCETChatbotView, basename="kcet_chatbot")
router.register("key-statistics", KeyStatisticsViewSet, basename="key-statistics")
router.register("quick-links", QuickLinksViewSet, basename="quick-links")
router.register("search", CollegeSearchViewSet, basename="search")
router.register("cutoff-analytics", CutoffAnalyticsViewSet, basename="cutoff-analytics")
router.register("seatmatrix-analytics", SeatMatrixAnalyticsViewSet, basename="seatmatrix-analytics")
path("search/", CollegeSearchViewSet.as_view({"get": "list"})),
router.register("cutoff-table", CutoffRanksViewSet, basename="cutoff-table")
'''path("search/", search_suggestions),
path("colleges/", CollegeListView.as_view()),
path("cutoff/", CutoffView.as_view()),
path("seatmatrix/", SeatMatrixView.as_view()),
path("stats/", StatsView.as_view()),'''

urlpatterns = router.urls
