from django.urls import path
from tensorboards import views

urlpatterns = [
    path('tensorboards', views.TensorboardList.as_view()),
]
