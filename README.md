# Shopify Product Taxonomy Classifier

 Built with Python, Django, Django REST Framework, Microsoft SQL Server, HTML/CSS/JavaScript, Pandas and Celery/Redis.

# Sample
The supplied Product List.xlsx contains 4,999 products and 48 columns. Existing Product Category/Product Sub Category are retained as reference/evaluation fields, not simply returned as the Shopify prediction.

# Setup
1. Create SQL Server database:
   CREATE DATABASE ShopifyClassifier;
2. set SQL Server credentials.
3. Install: 
    1) install python above 3.12 version and
    2) activate the scripts and
    3) install all version of pip format in requirements.txt 
4. Run `python manage.py makemigrations` and `python manage.py migrate`
5. Run `python manage.py import_sample`
6. Run `python manage.py runserver`
7. Open http://127.0.0.1:8000/

For background processing, start Redis and:
`celery -A config worker -l info --pool=solo`

# Classification
The prototype uses explainable TF-IDF similarity against taxonomy breadcrumbs, structured fields, simple attribute extraction, confidence thresholds and alternative categories. Image URLs are validated/used as an additional text signal; a production deployment can replace this with CLIP or another vision model.

# Resume/fault tolerance
Products have PENDING, PROCESSING, COMPLETED, FAILED and REVIEW_REQUIRED states. Celery retries failed work, and the batch only queues pending/failed products, so completed products are not restarted.

# API
GET /api/dashboard/
GET /api/products/
GET /api/classifications/
POST /api/process/
POST /api/classifications/<id>/approve/
POST /api/classifications/<id>/review/

# Shopify taxonomy
Use the official Shopify Standard Product Taxonomy distribution for production taxonomy loading. 
The small CATEGORY_MAP in `classification/engine.py` is a runnable prototype mapping for this furniture sample.
