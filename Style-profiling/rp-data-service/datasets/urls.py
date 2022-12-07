from django.urls import path
from datasets import views

urlpatterns = [
    path('datasets/status', views.DatasetStatusList.as_view()),
    path('datasets/customers', views.DatasetCustomerList.as_view()),
    path('datasets/products', views.DatasetProductList.as_view()),
    path('datasets/products/autocomplete', views.DatasetProductAutocomplete.as_view()),
    path('datasets/products/<str:id>', views.DatasetProductDetail.as_view()), 
    path('datasets/historys', views.DatasetHistoryList.as_view()),
]
