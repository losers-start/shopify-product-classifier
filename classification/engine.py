import re
from collections import Counter
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from products.models import *
from products.services import image_text_signal

CATEGORY_MAP = {
    "Sofa Sectionals": "Furniture > Living Room Furniture > Sofas",
    "Sofas and Armchairs": "Furniture > Living Room Furniture > Sofas",
    "Dining Chairs": "Furniture > Chairs",
    "Bar and Counter Stools": "Furniture > Chairs > Stools",
    "Bar and Dining Tables": "Furniture > Tables",
    "Dining Sets": "Furniture > Dining Sets",
    "Tables": "Furniture > Tables",
    "Vanities": "Furniture > Cabinets & Storage",
    "Office Chairs": "Furniture > Office Furniture > Office Chairs",
    "Computer Desks": "Furniture > Office Furniture > Desks",
    "Benches and Stools": "Furniture > Benches",
    "Daybeds and Lounges": "Furniture > Beds & Bed Frames",
    "Ceiling Lamps": "Home & Garden > Lighting > Ceiling Lighting",
    "Table Lamps": "Home & Garden > Lighting > Lamps",
    "Floor Lamps": "Home & Garden > Lighting > Floor Lamps",
    "Decor": "Home & Garden > Decor",
    "Pillow": "Home & Garden > Decor > Pillows",
    "Case Goods": "Furniture > Cabinets & Storage",
    "Bar and Dining": "Furniture > Dining Furniture",
}


def norm(v):
    return re.sub(r"\s+", " ", str(v or "").lower()).strip()


def ensure_seed_taxonomy():
    for _, breadcrumb in CATEGORY_MAP.items():
        parts = [x.strip() for x in breadcrumb.split(">")]
        parent = None
        for level, name in enumerate(parts, 1):
            sid = "prototype:" + ":".join(
                re.sub(r"[^a-z0-9]+", "-", x.lower()).strip("-") for x in parts[:level]
            )
            obj, _ = TaxonomyCategory.objects.get_or_create(
                shopify_id=sid,
                defaults={
                    "name": name,
                    "breadcrumb": " > ".join(parts[:level]),
                    "parent": parent,
                    "level": level,
                },
            )
            if obj.parent_id != (parent.id if parent else None):
                obj.parent = parent
                obj.save(update_fields=["parent"])
            parent = obj


def build_text(p):
    vals = [
        p.product_name,
        p.product_description,
        p.bullets,
        p.materials,
        p.source_category,
        p.source_sub_category,
        p.collection_name,
        p.product_color,
        image_text_signal(p),
    ]
    return " ".join(norm(x) for x in vals if x)


def extract_attributes(p):
    d = {}
    for key, field in {
        "material": "materials",
        "color": "product_color",
        "assembly_required": "assembly_required",
        "is_set": "is_set",
        "stackable": "stackable",
        "country_of_origin": "country_of_origin",
    }.items():
        v = getattr(p, field, "")
        if v:
            d[key] = v
    return d


def classify_product(p):
    ensure_seed_taxonomy()
    cats = list(TaxonomyCategory.objects.filter(is_active=True))
    text = build_text(p)
    if not text:
        raise ValueError("No usable product data.")
    corpus = [norm(c.breadcrumb) for c in cats]
    vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    mat = vec.fit_transform(corpus + [text])
    raw = cosine_similarity(mat[-1], mat[:-1]).ravel()
    ranked = []
    source = norm(p.source_sub_category)
    title = norm(p.product_name)
    for c, s in zip(cats, raw):
        score = float(s)
        if source and any(norm(x) in norm(c.breadcrumb) for x in source.split()):
            score += 0.35
        if title and norm(c.name) in title:
            score += 0.20
        ranked.append((c, min(score, 1.0)))
    ranked.sort(key=lambda x: x[1], reverse=True)
    top, score = ranked[0]
    evidence = Counter(re.findall(r"[a-z]{3,}", text))
    if len(evidence) < 2:
        score = min(score, 0.55)
    status = (
        "AUTO_APPROVED"
        if score >= settings.CLASSIFICATION_AUTO_APPROVE
        else "REVIEW_REQUIRED"
    )
    result, _ = ClassificationResult.objects.update_or_create(
        product=p,
        defaults={
            "predicted_category": top,
            "confidence_score": Decimal(str(round(score, 4))),
            "status": status,
            "attributes": extract_attributes(p),
            "alternatives": [
                {
                    "category_id": c.id,
                    "category": c.breadcrumb,
                    "confidence": round(s, 4),
                }
                for c, s in ranked[1:4]
            ],
            "signals": {
                "title": bool(p.product_name),
                "description": bool(p.product_description),
                "materials": bool(p.materials),
                "image_count": len(p.image_urls or []),
            },
            "processed_at": datetime.now(),
            "error_message": "",
        },
    )
    p.processing_status = (
        "COMPLETED" if status == "AUTO_APPROVED" else "REVIEW_REQUIRED"
    )
    p.processing_attempts += 1
    p.last_error = ""
    p.save(
        update_fields=[
            "processing_status",
            "processing_attempts",
            "last_error",
            "updated_at",
        ]
    )
    if status == "REVIEW_REQUIRED":
        ManualReview.objects.update_or_create(
            product=p,
            defaults={
                "reason": f"Confidence {score:.2%} below auto-approval threshold.",
                "status": "OPEN",
            },
        )
    return result
