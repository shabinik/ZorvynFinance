from django.urls import path
 
from .views import (
    CategoryBreakdownView,
    DashboardSummaryView,
    MonthlyTrendsView,
    RecentActivityView,
    RecordTypeSplitView
)
 
urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="analytics-summary"),
    path("categories/", CategoryBreakdownView.as_view(), name="analytics-categories"),
    path("trends/monthly/", MonthlyTrendsView.as_view(), name="analytics-monthly"),
    path("recent/", RecentActivityView.as_view(), name="analytics-recent"),
    path("split/", RecordTypeSplitView.as_view(), name="analytics-split"),
]