from django.urls import path
from pages import views

urlpatterns = [
    path('pages', views.PageList.as_view()),
    path('pages/count', views.PageCount.as_view()),  # /count path가 /id보다 앞에 배치되어야 함.
    path('pages/reindex', views.Reindex.as_view()),
    path('pages/<str:id>', views.PageDetail.as_view()), 

]
