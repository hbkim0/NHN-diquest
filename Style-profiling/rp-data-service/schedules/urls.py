from django.urls import path
from schedules import views

urlpatterns = [
    path('schedules', views.ScheduleList.as_view()),
]
