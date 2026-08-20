from celery import shared_task
from django.db import close_old_connections
from products.models import Product
from .engine import classify_product


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def classify_product_task(self, product_id):
    close_old_connections()
    try:
        p = Product.objects.get(pk=product_id)
        if p.processing_status == "COMPLETED":
            return {"status": "skipped"}
        p.processing_status = "PROCESSING"
        p.save(update_fields=["processing_status", "updated_at"])
        classify_product(p)
        return {"status": "done", "product_id": product_id}
    except Exception as e:
        try:
            p = Product.objects.get(pk=product_id)
            p.processing_status = "FAILED"
            p.processing_attempts += 1
            p.last_error = str(e)
            p.save(
                update_fields=[
                    "processing_status",
                    "processing_attempts",
                    "last_error",
                    "updated_at",
                ]
            )
        except Product.DoesNotExist:
            pass
        raise self.retry(exc=e)


@shared_task
def process_products_task(batch_size=100):
    ids = list(
        Product.objects.filter(processing_status__in=["PENDING", "FAILED"]).values_list(
            "id", flat=True
        )[:10000]
    )
    for i in range(0, len(ids), batch_size):
        for pid in ids[i : i + batch_size]:
            classify_product_task.delay(pid)
    return {"queued": len(ids)}
