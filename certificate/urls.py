from django.urls import path, include

from .views import *


urlpatterns = [
    path('demands/<int:pk>/', DemandListView.as_view(), name="demand-list"),
    path('demand_create/<int:pk>/', DemandCreateView.as_view(), name="demand-create"),
    path('demand_update/<int:pk>/', DemandUpdateView.as_view(), name="demand-update"),
    path('update_certificate/<int:course_pk>/', update_certificate, name="update_certificate"),
    path('download_document/<int:pk>/', download_document, name="download_document"),
]