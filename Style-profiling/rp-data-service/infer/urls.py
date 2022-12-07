from django.urls import path
from infer import views

urlpatterns = [
    path('infer/text', views.InferText.as_view()), 
    path('infer/image', views.InferImage.as_view()), 
]
