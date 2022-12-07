from django.urls import path
from workbooks import views

urlpatterns = [
    path('workbooks', views.WorkbookList.as_view()), 
    path('workbooks/<str:id>', views.WorkbookDetail.as_view()), 
]
