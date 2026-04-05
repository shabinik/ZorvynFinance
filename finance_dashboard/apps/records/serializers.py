from rest_framework import serializers
from .models import Category, FinancialRecord
from datetime import date


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = "__all__"
        read_only_fields = ["created_by"]


    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Future dates are not allowed")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    def validate(self, attrs):
        category = attrs.get("category")
        record_type = attrs.get("record_type")

        if category and record_type and category.record_type != record_type:
            raise serializers.ValidationError(
                "Category type does not match record type"
            )

        return attrs


class FinancialRecordReadSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = FinancialRecord
        fields = [
            "id",
            "amount",
            "record_type",
            "category",
            "category_name",
            "date",
            "description",
            "created_by",
            "created_at",
        ]