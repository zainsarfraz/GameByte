
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('',landingPage,name='landingpage'),
    path('googleAuth', googleAuthTest,name='googleAuthTest'),
    path('checkUser',checkUser,name='checkUser'),
    path('register',register,name='register'),
    path('playground',playground,name='playground'),
    path('dashboard',dashboard,name='dashboard'),
    path('problems',problems,name='problems'),
    path('profile',user_profile,name='profile'),
]
