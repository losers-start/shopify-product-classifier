from django.db import models


class TaxonomyCategory(models.Model):
    shopify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    breadcrumb = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="children"
    )
    level = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["name"]), models.Index(fields=["parent"])]

    def __str__(self):
        return self.breadcrumb


class CategoryAttribute(models.Model):
    shopify_id = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        TaxonomyCategory, on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField(max_length=255)


class AttributeValue(models.Model):
    shopify_id = models.CharField(max_length=255, unique=True)
    attribute = models.ForeignKey(
        CategoryAttribute, on_delete=models.CASCADE, related_name="values"
    )
    name = models.CharField(max_length=255)


class Product(models.Model):
    STATUS = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REVIEW_REQUIRED", "Review Required"),
    ]
    product_number = models.CharField(max_length=255, unique=True)
    model_number = models.CharField(max_length=255, blank=True)
    source_category = models.CharField(max_length=255, blank=True)
    source_sub_category = models.CharField(max_length=255, blank=True)
    collection_name = models.CharField(max_length=255, blank=True)
    product_color = models.CharField(max_length=255, blank=True)
    product_name = models.CharField(max_length=500, blank=True)
    product_description = models.TextField(blank=True)
    bullets = models.TextField(blank=True)
    materials = models.TextField(blank=True)
    product_dimensions = models.TextField(blank=True)
    assembly_required = models.CharField(max_length=100, blank=True)
    is_set = models.CharField(max_length=100, blank=True)
    stackable = models.CharField(max_length=100, blank=True)
    country_of_origin = models.CharField(max_length=255, blank=True)
    product_url = models.URLField(blank=True, max_length=1000)
    image_urls = models.JSONField(default=list, blank=True)
    image_status = models.CharField(max_length=50, default="NOT_CHECKED")
    processing_status = models.CharField(
        max_length=30, choices=STATUS, default="PENDING"
    )
    processing_attempts = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["processing_status"]),
            models.Index(fields=["source_category"]),
            models.Index(fields=["product_name"]),
        ]


class ClassificationResult(models.Model):
    STATUS = [
        ("AUTO_APPROVED", "Auto Approved"),
        ("REVIEW_REQUIRED", "Review Required"),
        ("MANUALLY_APPROVED", "Manually Approved"),
    ]
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="classification"
    )
    predicted_category = models.ForeignKey(
        TaxonomyCategory, null=True, blank=True, on_delete=models.SET_NULL
    )
    confidence_score = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    status = models.CharField(max_length=30, choices=STATUS, default="REVIEW_REQUIRED")
    attributes = models.JSONField(default=dict, blank=True)
    alternatives = models.JSONField(default=list, blank=True)
    signals = models.JSONField(default=dict, blank=True)
    classifier_version = models.CharField(max_length=50, default="tfidf-v1")
    error_message = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)


class ManualReview(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="manual_review"
    )
    reason = models.CharField(max_length=500)
    reviewer = models.CharField(max_length=255, blank=True)
    selected_category = models.ForeignKey(
        TaxonomyCategory, null=True, blank=True, on_delete=models.SET_NULL
    )
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=30, default="OPEN")
    reviewed_at = models.DateTimeField(null=True, blank=True)
