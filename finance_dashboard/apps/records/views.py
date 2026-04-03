from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from . models import Category, FinancialRecord
from . serializers import (
    CategorySerializer,
    FinancialRecordSerializer,
    FinancialRecordReadSerializer,
)
from . filters import FinancialRecordFilter
from apps.users.permissions import IsAdminOrReadOnly
from apps.core.responses import success
from rest_framework.decorators import action

# Create your views here.

# CATEGORY
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active = True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    filterset_class = FinancialRecordFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ["description"]
    ordering_fields = ["date", "amount"]
    ordering = ["-date"]

    def get_queryset(self):
        qs = FinancialRecord.objects.select_related("category", "created_by")

        include_deleted = self.request.query_params.get("include_deleted")

        if include_deleted == "true" and self.request.user.role == "admin":
            qs = FinancialRecord.all_objects.select_related("category", "created_by")

        return qs

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FinancialRecordReadSerializer
        return FinancialRecordSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        record.soft_delete()
        return success(message="Record deleted")
    

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        record = FinancialRecord.all_objects.get(pk=pk)
        record.is_deleted = False
        record.save()
        return success(message="Record restored")