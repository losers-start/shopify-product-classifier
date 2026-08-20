from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("import/", views.import_products, name="import_products"),
    path("process/", views.start_processing, name="start_processing"),
]
