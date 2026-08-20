from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from products.services import import_dataframe


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        p = Path("data") / "Product List.xlsx"
        df = pd.read_excel(p)
        a, b = import_dataframe(df)
        self.stdout.write(self.style.SUCCESS(f"Imported {a} new and updated {b}."))
