import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CategoryAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shopify_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="AttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shopify_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="values",
                        to="products.categoryattribute",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_number", models.CharField(max_length=255, unique=True)),
                ("model_number", models.CharField(blank=True, max_length=255)),
                ("source_category", models.CharField(blank=True, max_length=255)),
                ("source_sub_category", models.CharField(blank=True, max_length=255)),
                ("collection_name", models.CharField(blank=True, max_length=255)),
                ("product_color", models.CharField(blank=True, max_length=255)),
                ("product_name", models.CharField(blank=True, max_length=500)),
                ("product_description", models.TextField(blank=True)),
                ("bullets", models.TextField(blank=True)),
                ("materials", models.TextField(blank=True)),
                ("product_dimensions", models.TextField(blank=True)),
                ("assembly_required", models.CharField(blank=True, max_length=100)),
                ("is_set", models.CharField(blank=True, max_length=100)),
                ("stackable", models.CharField(blank=True, max_length=100)),
                ("country_of_origin", models.CharField(blank=True, max_length=255)),
                ("product_url", models.URLField(blank=True, max_length=1000)),
                ("image_urls", models.JSONField(blank=True, default=list)),
                (
                    "image_status",
                    models.CharField(default="NOT_CHECKED", max_length=50),
                ),
                (
                    "processing_status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("PROCESSING", "Processing"),
                            ("COMPLETED", "Completed"),
                            ("FAILED", "Failed"),
                            ("REVIEW_REQUIRED", "Review Required"),
                        ],
                        default="PENDING",
                        max_length=30,
                    ),
                ),
                ("processing_attempts", models.PositiveIntegerField(default=0)),
                ("last_error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["processing_status"],
                        name="products_pr_process_7d7449_idx",
                    ),
                    models.Index(
                        fields=["source_category"],
                        name="products_pr_source__99b9e7_idx",
                    ),
                    models.Index(
                        fields=["product_name"], name="products_pr_product_097795_idx"
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="TaxonomyCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shopify_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("breadcrumb", models.TextField()),
                ("level", models.PositiveIntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="products.taxonomycategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ManualReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reason", models.CharField(max_length=500)),
                ("reviewer", models.CharField(blank=True, max_length=255)),
                ("notes", models.TextField(blank=True)),
                ("status", models.CharField(default="OPEN", max_length=30)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="manual_review",
                        to="products.product",
                    ),
                ),
                (
                    "selected_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.taxonomycategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClassificationResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "confidence_score",
                    models.DecimalField(decimal_places=4, default=0, max_digits=6),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AUTO_APPROVED", "Auto Approved"),
                            ("REVIEW_REQUIRED", "Review Required"),
                            ("MANUALLY_APPROVED", "Manually Approved"),
                        ],
                        default="REVIEW_REQUIRED",
                        max_length=30,
                    ),
                ),
                ("attributes", models.JSONField(blank=True, default=dict)),
                ("alternatives", models.JSONField(blank=True, default=list)),
                ("signals", models.JSONField(blank=True, default=dict)),
                (
                    "classifier_version",
                    models.CharField(default="tfidf-v1", max_length=50),
                ),
                ("error_message", models.TextField(blank=True)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="classification",
                        to="products.product",
                    ),
                ),
                (
                    "predicted_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.taxonomycategory",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="categoryattribute",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attributes",
                to="products.taxonomycategory",
            ),
        ),
        migrations.AddIndex(
            model_name="taxonomycategory",
            index=models.Index(fields=["name"], name="products_ta_name_1c6be8_idx"),
        ),
        migrations.AddIndex(
            model_name="taxonomycategory",
            index=models.Index(
                fields=["parent"], name="products_ta_parent__f268c7_idx"
            ),
        ),
    ]
