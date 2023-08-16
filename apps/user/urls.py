"""application admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from .views import *

urlpatterns = [
    # Admin
    path('admin/user/add', CreateUserView.as_view(), name='admin-user-add'),
    path('admin/user/', ListUserView.as_view(), name='admin-user-list'),
    path('admin/user/list/ajax', ListUserViewJson.as_view(), name='admin-user-list-ajax'),
    path('admin/user/edit/<int:pk>', UpdateUserView.as_view(), name='admin-user-edit'),
    path('admin/user/delete/<int:pk>', DeleteUserView.as_view(), name='admin-user-delete'),


]
