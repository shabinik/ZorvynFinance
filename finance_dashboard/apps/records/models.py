from django.db import models
from django.conf import settings

from apps.core.models import SoftDeleteModel,SoftDeleteManager,TimeStampedModel

# Create your models here.

class RecordType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = 'expense', "Expense"


# Transaction categories (e.g. Salary, Rent, Utilities, Food).- GLOBAL VIEW
class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    record_type = models.CharField(
        max_length=10,
        choices=RecordType.choices,
        help_text="The type of transaction this category is associated with.",
    )
    is_active = models.BooleanField(default=True)
 
    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
 
    def __str__(self):
        return f"{self.name} ({self.record_type})"
    



class FinancialRecord(TimeStampedModel,SoftDeleteModel):
    amount = models.DecimalField(max_digits=12,decimal_places=2,help_text="Transaction amount, Always postive value",)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="records", null=True, blank=True)
    date = models.DateField(db_index=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_records",
    )
    record_type = models.CharField(
        max_length=10,
        choices=RecordType.choices,
        db_index=True
    )

    objects = SoftDeleteManager()        # only non-deleted
    all_objects = models.Manager()       # includes deleted
 
    class Meta:
        db_table = "financial_records"
        verbose_name = "Financial Record"
        verbose_name_plural = "Financial Records"
        ordering = ["-date", "-created_at"]
        indexes = [
            # Composite index for the most common dashboard query pattern:
            # filtering by type + date range
            models.Index(fields=["record_type", "date"], name="idx_record_type_date"),
            models.Index(fields=["date", "is_deleted"], name="idx_date_not_deleted"),
        ]
 
    def __str__(self):
        return f"{self.record_type.upper()} | {self.amount} | {self.date}"
