from django.urls import path
from files import views

urlpatterns = [
    path('files/upload', views.FileList.as_view()),
    path('files/<str:id>', views.FileDetail.as_view()), 
]