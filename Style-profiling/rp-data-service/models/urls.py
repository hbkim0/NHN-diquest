from django.urls import path
from models import views

urlpatterns = [
    path('models', views.ModelList.as_view()),
]