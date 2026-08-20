import re, requests
from pathlib import Path
from urllib.parse import urlparse
from django.db import transaction

COLUMN_MAP = {
    "Product Number": "product_number",
    "Model Number": "model_number",
    "Product Category": "source_category",
    "Product Sub Category": "source_sub_category",
    "Collection Name": "collection_name",
    "Product Color": "product_color",
    "Product Name": "product_name",
    "Product Description ": "product_description",
    "Bullets": "bullets",
    "Materials": "materials",
    "Product Dimensions": "product_dimensions",
    "Assembly Required": "assembly_required",
    "Is a Set": "is_set",
    "Stackable": "stackable",
    "Country Of Origin": "country_of_origin",
    "Product URL": "product_url",
}


def clean(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.lower() in {"nan", "none", "nat"} else s


def import_dataframe(df):
    image_cols = [c for c in df.columns if str(c).lower().startswith("image ")]
    created = updated = 0
    for _, row in df.iterrows():
        pn = clean(row.get("Product Number"))
        if not pn:
            continue
        defaults = {}
        for source, target in COLUMN_MAP.items():
            if source in df.columns:
                defaults[target] = clean(row.get(source))
        defaults["image_urls"] = [
            clean(row.get(c)) for c in image_cols if clean(row.get(c))
        ]
        from .models import Product

        with transaction.atomic():
            _, new = Product.objects.update_or_create(
                product_number=pn, defaults=defaults
            )
        created += int(new)
        updated += int(not new)
    return created, updated


def validate_image(url, timeout=8):
    if not url:
        return False, "EMPTY"
    try:
        r = requests.get(
            url,
            timeout=timeout,
            stream=True,
            headers={"User-Agent": "ShopifyClassifier/1.0"},
        )
        r.raise_for_status()
        if not r.headers.get("Content-Type", "").startswith("image/"):
            return False, "NOT_IMAGE"
        return True, "OK"
    except requests.RequestException as e:
        return False, type(e).__name__


def image_text_signal(product):
    tokens = []
    for url in (product.image_urls or [])[:5]:
        name = re.sub(r"[^a-z0-9]+", " ", urlparse(url).path.lower())
        tokens.extend(name.split())
    return " ".join(tokens)
