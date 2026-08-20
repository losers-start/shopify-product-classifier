# Shopify Product Taxonomy Classifier

An intelligent and explainable product classification system built with **Python, Django, Django REST Framework, Microsoft SQL Server, Pandas, Celery, Redis, HTML, CSS, and JavaScript**.

The application imports product data from Excel, analyzes product information, and recommends the most appropriate **Shopify Standard Product Taxonomy** category using explainable text-similarity techniques.

It also provides confidence scores, alternative category suggestions, review workflows, background processing, and fault-tolerant batch classification.

---

## 📌 Project Overview

The Shopify Product Taxonomy Classifier is designed to automatically classify large product catalogs into appropriate Shopify taxonomy categories.

The system accepts product information such as:

- Product Name
- Product Title
- Product Description
- Product Category
- Product Sub Category
- Product Type
- Brand
- Material
- Color
- Size
- Gender
- Image URL
- Other structured product attributes

The classifier combines these fields and compares the product information against available taxonomy categories and their breadcrumbs.

Instead of returning only a prediction, the system provides an **explainable classification result** with:

- Recommended Shopify category
- Confidence score
- Alternative categories
- Classification status
- Review status
- Processing information

Existing `Product Category` and `Product Sub Category` fields from the sample Excel file are retained as **reference/evaluation fields** and are not blindly returned as the Shopify prediction.

---

# 🚀 Key Features

## 1. Excel Product Import

The application supports importing product catalog data from Excel files.

The supplied sample file contains:

- **4,999 products**
- **48 columns**

Pandas is used to read and process the Excel data before storing it in the database.

---

## 2. Automated Product Classification

Products are automatically classified using an explainable classification engine.

The prototype uses:

- TF-IDF vectorization
- Cosine similarity
- Taxonomy breadcrumb matching
- Product title matching
- Product description matching
- Structured product attributes
- Simple attribute extraction
- Confidence thresholds
- Alternative category recommendations

---

## 3. Explainable Predictions

The classifier does not simply return a category.

For each classification, the system can provide information such as:

```text
Product:
Modern Wooden Dining Table

Predicted Category:
Furniture > Tables > Dining Tables

Confidence:
87.4%

Alternative Categories:
Furniture > Tables
Furniture > Kitchen & Dining Furniture

Status:
COMPLETED
