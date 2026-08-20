from django.db.models import Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import *
from .engine import classify_product
from .serializers import *
from .tasks import process_products_task


class DashboardAPI(APIView):
    def get(self, request):
        d = {
            x["processing_status"]: x["total"]
            for x in Product.objects.values("processing_status").annotate(
                total=Count("id")
            )
        }
        d["total"] = Product.objects.count()
        return Response(d)


class ProductAPI(APIView):
    def get(self, request):
        q = request.query_params.get("q", "")
        qs = Product.objects.all().order_by("-updated_at")
        if q:
            qs = qs.filter(product_name__icontains=q)
        return Response(ProductSerializer(qs[:200], many=True).data)


class ClassificationAPI(APIView):
    def get(self, request):
        qs = ClassificationResult.objects.select_related("predicted_category").order_by(
            "-processed_at"
        )
        if request.query_params.get("status"):
            qs = qs.filter(status=request.query_params["status"])
        return Response(ClassificationResultSerializer(qs[:200], many=True).data)


class ApproveAPI(APIView):
    def post(self, request, pk):
        r = ClassificationResult.objects.select_related("product").get(pk=pk)
        r.status = "MANUALLY_APPROVED"
        r.product.processing_status = "COMPLETED"
        r.product.save(update_fields=["processing_status", "updated_at"])
        r.save(update_fields=["status"])
        ManualReview.objects.filter(product=r.product).update(
            status="APPROVED",
            reviewer=request.data.get("reviewer", "interviewer"),
            reviewed_at=timezone.now(),
        )
        return Response(ClassificationResultSerializer(r).data)


class ReviewAPI(APIView):
    def post(self, request, pk):
        r = ClassificationResult.objects.select_related("product").get(pk=pk)
        cid = request.data.get("category_id")
        if cid:
            r.predicted_category = TaxonomyCategory.objects.get(pk=cid)
        r.status = "MANUALLY_APPROVED"
        r.product.processing_status = "COMPLETED"
        r.product.save(update_fields=["processing_status", "updated_at"])
        r.save(update_fields=["predicted_category", "status"])
        ManualReview.objects.update_or_create(
            product=r.product,
            defaults={
                "reason": "Manual review",
                "reviewer": request.data.get("reviewer", "interviewer"),
                "notes": request.data.get("notes", ""),
                "status": "APPROVED",
                "reviewed_at": timezone.now(),
                "selected_category": r.predicted_category,
            },
        )
        return Response(ClassificationResultSerializer(r).data)


class ProcessAPI(APIView):
    def post(self, request):
        pid = request.data.get("product_id")
        if pid:
            return Response(
                ClassificationResultSerializer(
                    classify_product(Product.objects.get(pk=pid))
                ).data
            )
        job = process_products_task.delay()
        return Response(
            {"task_id": job.id, "message": "Batch queued"},
            status=status.HTTP_202_ACCEPTED,
        )
