from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth, TruncWeek
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.records.models import FinancialRecord, RecordType
from apps.records.serializers import FinancialRecordReadSerializer
from apps.users.permissions import IsAnalystOrAdmin
from apps.core.responses import success

# Create your views here.

# SUMMARY
class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        qs = FinancialRecord.objects.all()

        income = qs.filter(record_type = "income").aggregate(total = Sum("amount"))["total"] or 0
        expense = qs.filter(record_type = "expense").aggregate(total = Sum("amount"))["total"] or 0

        return success({
            "total_income": income,
            "total_expense": expense,
            "balance": income - expense,
            "count": qs.count(),
        })
    
#  BREAKDOWN BY CATEGORY
class CategoryBreakdownView(APIView):
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self,request):
        data = (
            FinancialRecord.objects
            .values("category__name","record_type")
            .annotate(total = Sum("amount"), count = Count("id"))
            .order_by("-total")
        )

        return success(list(data))

# MONTHLY TRENDS
class MonthlyTrendsView(APIView):
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        data = (
            FinancialRecord.objects
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(
                income=Sum("amount", filter=Q(record_type="income")),
                expense=Sum("amount", filter=Q(record_type="expense")),
            )
            .order_by("month")
        )

        return success(list(data))


# RECENT ACTIVITY
class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))

        records = (
            FinancialRecord.objects
            .select_related("category", "created_by")
            .order_by("-date")[:limit]
        )

        return success(FinancialRecordReadSerializer(records, many=True).data)


# INCOME vs EXPENSE SPLIT
class RecordTypeSplitView(APIView):
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        qs = FinancialRecord.objects.all()

        income = qs.filter(record_type="income").aggregate(total=Sum("amount"))["total"] or 0
        expense = qs.filter(record_type="expense").aggregate(total=Sum("amount"))["total"] or 0

        total = income + expense

        return success({
            "income": {
                "total": income,
                "percentage": (income / total * 100) if total else 0
            },
            "expense": {
                "total": expense,
                "percentage": (expense / total * 100) if total else 0
            }
        })