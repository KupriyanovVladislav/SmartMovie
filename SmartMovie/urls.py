"""SmartMovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
import main.admin_views as admin_views
import main.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^admin_task/(?P<task_name>\w+)', admin_views.run_task, name='run_admin_task'),
    path('', views.Index.as_view(), name='index'),
    path('api/', include('main.urls')),
]
