
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', googleAuthTest,name='googleAuthTest'),
    path('checkUser',checkUser,name='checkUser'),
]
