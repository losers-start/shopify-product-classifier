from django.contrib import admin
from .models import *

admin.site.register(
    [
        TaxonomyCategory,
        CategoryAttribute,
        AttributeValue,
        ClassificationResult,
        ManualReview,
    ]
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_number",
        "product_name",
        "processing_status",
        "image_status",
    )
    list_filter = ("processing_status", "image_status")
    search_fields = ("product_number", "product_name", "model_number")
