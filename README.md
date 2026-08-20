# Shopify Product Taxonomy Classifier

An intelligent and explainable product classification system built with **Python, Django, Django REST Framework, Microsoft SQL Server, Pandas, Celery, Redis, HTML, CSS, and JavaScript**.

The application imports product data from Excel, analyzes product information, and recommends the most appropriate **Shopify Standard Product Taxonomy** category using explainable text-similarity techniques.

It also provides confidence scores, alternative category suggestions, review workflows, background processing, and fault-tolerant batch classification.

---

##  Project Overview

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

#  Key Features

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

---

** ## 4. Confidence-Based Review **

Classification results are evaluated using confidence thresholds.
Depending on the confidence score, a product can be:

  1) Automatically completed
  2) Sent for manual review
  3) Marked as failed

Example:
Confidence >= 80%
        ↓
   COMPLETED

Confidence < 80%
        ↓
 REVIEW_REQUIRED

This allows uncertain predictions to be reviewed by users instead of automatically accepting low-confidence results

---

## ** 5. Product Processing Workflow **

                Excel File
                    |
                    v
              Product Import
                    |
                    v
             SQL Server DB
                    |
                    v
          Pending Products
                    |
                    v
          Celery Background Job
                    |
                    v
        Classification Engine
                    |
          +---------+---------+
          |                   |
          v                   v
    High Confidence      Low Confidence
          |                   |
          v                   v
      COMPLETED         REVIEW_REQUIRED
          |                   |
          +---------+---------+
                    |
                    v
             User Review
                    |
                    v
              Final Result

---

## ** 6. Technology Stack **

Python - Backend programming
Django - Web application framework
Django REST Framework -	REST API development
Microsoft SQL Server	- Database
mssql-django - Django SQL Server integration
pyodbc -	SQL Server connectivity
Pandas -	Excel/data processing
OpenPyXL-	Excel file handling
Celery -	Background task processing
Redis -	Celery message broker
HTML -	Frontend structure
CSS -	Frontend styling
JavaScript -	Frontend interaction
Bootstrap -	Responsive UI

---

## ** 7. Classification Engine **

The classification process uses product information and taxonomy breadcrumbs to determine similarity.

 Step 1 : Product Text Preparation - Relevant product fields are combined into a searchable text representation.
 Step 2 : Taxonomy Text Preparation - Each taxonomy category is represented using its breadcrumb.
 Step 3 : TF-IDF Vectorization - The system converts product text and taxonomy text into numerical TF-IDF vectors.TF-IDF               helps identify important words and reduces the influence of common words.
 Step 4 : Similarity Calculation - Cosine similarity is used to compare the product representation with taxonomy                       representations.
 Step 5 : Confidence Evaluation - The highest-scoring taxonomy category is selected as the recommended category.The                    confidence score is then evaluated against configured thresholds.
 Step 6 : Alternative Categories - The classifier also keeps alternative category suggestions.

---

## ** 8. Image URL Support **

Image URLs can also be used as an additional product signal.The prototype validates image URLs and incorporates available image-related information into the classification workflow.The current implementation is intentionally lightweight and explainable.

For a production-grade system, the image classification component can be replaced or extended with computer vision models such as:
  1) CLIP
  2) Vision Transformers
  3) Image Embedding Models
  4) Multimodal LLM-based classification

---

## ** 9. Product Status Management **

Each product can have one of the following processing states:
  PENDING - Product has been imported but has not yet been processed.
  PROCESSING - Product is currently being processed by a Celery worker.
  COMPLETED - Product has been successfully classified with sufficient confidence.
  FAILED - An error occurred during processing.
  REVIEW_REQUIRED - The classification confidence is below the configured threshold and requires manual validation.

---

## ** 10. Image Information **

Product image URLs can be validated and used as an additional signal in the classification workflow.
The current implementation does not depend on a heavy computer vision model, keeping the prototype simple and explainable.
For a production implementation, image understanding can be enhanced using:
    CLIP 
    Vision Transformers
    Image embeddings
    Multimodal models

---

## ** 11. Database Architecture **

Microsoft SQL Server is used as the primary database.

  The database stores information related to:
    Products
    Taxonomy categories
    Classification results
    Confidence scores
    Alternative categories
    Processing states
    Review information
    Classification history

---

## ** 12. REST API **

The project includes a Django REST Framework API for integrating the classification functionality with other applications.

---

## ** 13. Web Application **

  The frontend is built using:
    HTML
    CSS
    JavaScript
    Bootstrap
  The interface provides functionality for:
    Dashboard monitoring
    Product searching
    Product filtering
    Classification result viewing
    Confidence score viewing
    Review-required product identification
    Classification approval
    Processing status monitoring

---

## ** 14 . Evaluation Capability **

The existing product category and sub-category fields are retained as reference fields.
The project can therefore be extended to calculate:
    Top-1 accuracy
    Top-3 accuracy
    Precision
    Recall
    F1 score
    Confidence distribution
    Review rate
    Classification error rate
This evaluation layer is important for measuring how well the classifier performs before production deployment.












