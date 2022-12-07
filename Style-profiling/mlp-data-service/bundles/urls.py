from django.urls import path
from bundles import views

urlpatterns = [
    path('bundles', views.BundleList.as_view()), 
    path('bundles/<str:id>', views.BundleDetail.as_view()), 
]
