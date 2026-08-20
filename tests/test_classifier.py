from django.test import TestCase
from products.models import Product
from classification.engine import ensure_seed_taxonomy, classify_product


class ClassifierTests(TestCase):
    def setUp(self):
        ensure_seed_taxonomy()

    def test_title_only(self):
        p = Product.objects.create(
            product_number="T1",
            product_name="Dining Chair",
            source_sub_category="Dining Chairs",
        )
        r = classify_product(p)
        self.assertIsNotNone(r.predicted_category)
