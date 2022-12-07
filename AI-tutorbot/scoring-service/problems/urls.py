from django.urls import path
from problems import views

urlpatterns = [
    path('problems/explain', views.ProblemsExplain.as_view()),
]
