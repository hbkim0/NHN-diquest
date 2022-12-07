from django.urls import path
from annotations import views

urlpatterns = [
    path('annotations', views.AnnotationList.as_view()), 
    path('annotations/<str:id>', views.AnnotationDetail.as_view()), 
]
