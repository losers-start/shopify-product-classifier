from rest_framework import serializers
from products.models import Product, ClassificationResult


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ClassificationResultSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = ClassificationResult
        fields = [
            "id",
            "product",
            "predicted_category",
            "category",
            "confidence_score",
            "status",
            "attributes",
            "alternatives",
            "signals",
            "classifier_version",
            "error_message",
            "processed_at",
        ]

    def get_category(self, obj):
        return obj.predicted_category.breadcrumb if obj.predicted_category else None
