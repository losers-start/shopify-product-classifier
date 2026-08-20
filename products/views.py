from pathlib import Path
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product
from .services import import_dataframe
from classification.tasks import process_products_task


def dashboard(request):
    q = Product.objects.all()
    return render(
        request,
        "dashboard.html",
        {
            "total": q.count(),
            "completed": q.filter(processing_status="COMPLETED").count(),
            "review": q.filter(processing_status="REVIEW_REQUIRED").count(),
            "failed": q.filter(processing_status="FAILED").count(),
            "pending": q.filter(processing_status="PENDING").count(),
        },
    )


def product_list(request):
    qs = Product.objects.select_related("classification__predicted_category").order_by(
        "-updated_at"
    )
    q = request.GET.get("q", "").strip()
    st = request.GET.get("status", "").strip()
    if q:
        qs = qs.filter(product_name__icontains=q)
    if st:
        qs = qs.filter(processing_status=st)
    page = Paginator(qs, 25).get_page(request.GET.get("page"))
    return render(request, "products.html", {"page": page, "q": q, "status": st})


def product_detail(request, pk):
    return render(
        request,
        "review.html",
        {
            "product": get_object_or_404(
                Product.objects.select_related("classification__predicted_category"),
                pk=pk,
            )
        },
    )


def import_products(request):
    if request.method != "POST":
        return redirect("dashboard")
    f = request.FILES.get("file")
    if not f:
        messages.error(request, "Please select an Excel file.")
        return redirect("dashboard")
    temp = Path(settings.BASE_DIR) / "data" / "uploaded_products.xlsx"
    temp.parent.mkdir(exist_ok=True)
    with temp.open("wb+") as out:
        for chunk in f.chunks():
            out.write(chunk)
    created, updated = import_dataframe(pd.read_excel(temp))
    messages.success(request, f"Import complete: {created} created, {updated} updated.")
    return redirect("dashboard")


def start_processing(request):
    if request.method == "POST":
        process_products_task.delay()
    return redirect("dashboard")
