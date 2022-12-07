from django.urls import path
from versioned_datasets import views

urlpatterns = [
    path('versioned-datasets', views.VersionedDatasetList.as_view()), 
    path('versioned-datasets/<str:id>', views.VersionedDatasetDetail.as_view()), 
]