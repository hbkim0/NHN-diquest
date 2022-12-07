"""scoring_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schemas.urls')),
    path('', include('images.urls')),
    path('api/v1/', include('workbooks.urls')),
    path('api/v1/', include('pages.urls')),
    path('api/v1/', include('problems.urls')),
    path('api/v1/', include('infer.urls')),
    path('api/v1/', include('system.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
