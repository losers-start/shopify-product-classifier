from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard/", DashboardAPI.as_view()),
    path("products/", ProductAPI.as_view()),
    path("classifications/", ClassificationAPI.as_view()),
    path("classifications/<int:pk>/approve/", ApproveAPI.as_view()),
    path("classifications/<int:pk>/review/", ReviewAPI.as_view()),
    path("process/", ProcessAPI.as_view()),
]
