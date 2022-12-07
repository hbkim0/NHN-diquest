from django.urls import path
from images import views

urlpatterns = [
    path('images/upload', views.upload_images),
    path('images/<str:filename>', views.download_image),
]
