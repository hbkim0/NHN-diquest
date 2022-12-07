from django.urls import path
from functions import views

urlpatterns = [
    path('functions', views.FunctionList.as_view()), 
]
