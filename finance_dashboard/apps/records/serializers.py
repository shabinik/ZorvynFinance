from rest_framework import serializers
from .models import Category, FinancialRecord


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = "__all__"
        read_only_fields = ["created_by"]

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