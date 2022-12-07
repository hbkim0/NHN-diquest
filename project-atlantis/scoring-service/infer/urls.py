from django.urls import path
from infer import views

urlpatterns = [
    path('infer/dnr', views.InferDnR.as_view()), 
    path('infer/score', views.InferScore.as_view()), 
    path('logs', views.LogList.as_view()), 
]
