from django.urls import path
from students import views

urlpatterns = [
    path('students/<str:id>', views.StudentDetail.as_view()),
]
