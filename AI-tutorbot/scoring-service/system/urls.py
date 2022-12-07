from django.urls import path
from system import views

urlpatterns = [
    path('version', views.Version.as_view()),
]
