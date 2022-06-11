
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('',landingPage,name='landingpage'),
    #path('googleAuth', googleAuthTest,name='googleAuthTest'),
    path('checkUser',checkUser,name='checkUser'),
    path('register',register,name='register'),
    path('playground/<int:id>',playground,name='playground'),
    path('dashboard',dashboard,name='dashboard'),
    path('problems',problems,name='problems'),
    path('profile',user_profile,name='profile'),
    path('check_email',check_email,name='check_email'),
    path('check_username',check_username,name='check_username'),
    path('runtestcase',runtestcase,name='runtestcase'),
    path('about',about,name='about'),
    path('submitcode',submitcode,name='submitcode'),
    path('update_profile',update_profile,name='update_profile'),
    path('submissions',submissions,name='submissions'),
    path('downloadCode/<int:id>',downloadCode,name='downloadCode'),
    path('runCode/<int:id>',runCode,name='runCode'),
]
