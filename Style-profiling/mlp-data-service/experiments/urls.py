from django.urls import path
from experiments import views

urlpatterns = [
    path('experiments', views.ExperimentList.as_view()), 
    path('experiments/<str:id>', views.ExperimentDetail.as_view()), 
]
