from django.urls import path
from labels import views

urlpatterns = [
    path('labels', views.LabelList.as_view()), 
    path('labels/<str:id>', views.LabelDetail.as_view()), 
]
