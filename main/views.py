from urllib import request
from django.db.models.fields.files import ImageField
from django.http import HttpResponse
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.template import RequestContext, Template
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
from urllib.request import urlretrieve
from random import randint
from django.core.files.images import ImageFile
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login

def googleAuthTest(request):
    print(request.user)
    return render(request,'googleauthtest.html')

def checkUser(request):
    if UserDetails.objects.filter(user_id=request.user.id).exists():
        print("User Details of "+str(request.user)+" exists.")
    else:
        print("User Details of "+str(request.user)+" does not exists.")
        # imageName = randint(100000,999999)
        # urlretrieve(request.user.socialaccount_set.filter(provider='google')[0].extra_data['picture'],"media/google/"+str(imageName)+".jpg")
        userDetails = UserDetails(user_id=request.user)
        # userDetails.profile_pic = ImageFile(open("media/google/"+str(imageName)+".jpg","rb"))
        userDetails.save()

    return redirect('/profile')

def landingPage(request):
    return render(request,'landing_page.html')


def register(request):
    # i will add the user myself and authenticate it
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         new_user = form.save()
    #         messages.info(request, "Thanks for registering. You are now logged in.")
    #         new_user = authenticate(username=form.cleaned_data['username'],
    #                                 password=form.cleaned_data['password1'],
    #                                 )
    #         login(request, new_user)
    #         return HttpResponseRedirect("/dashboard/")
    # else:
    #     form = UserCreationForm()
    #     return render(request,"registration/signup.html", {
    #         'form': form,
    #     })
    if request.method == 'POST':
        usernmae = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        print(usernmae,email,password,password2,first_name,last_name)
        if password == password2:
            if User.objects.filter(username=usernmae).exists():
                messages.info(request, "Username already exists.")
                print("Username already exists.")
                return render(request,'registration/signup.html',{'error':'Username already exists.'})
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists.")
                print("Email already exists.")
                return render(request,'registration/signup.html',{'error':'Email already exists.'})
            else:
                user = User.objects.create_user(username=usernmae, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, "Thanks for registering. You are now logged in.")
                print("User created.")
                user = authenticate(username=usernmae, password=password)
                login(request, user)
                return redirect('/checkUser')
        else:
            messages.info(request, "Password not matching.")
            print("Password not matching.")
            return render(request,'registration/signup.html',{'error':'Password not matching.'})
    return render(request,'registration/signup.html')


def playground(request):
    if request.user.is_authenticated:
        return render(request,'playground.html')
    else:
        return redirect('/auth/login')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    else:
        return redirect('/auth/login')

def problems(request):
    if request.user.is_authenticated:
        return render(request,'problems.html')
    else:
        return redirect('/auth/login')


def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'user_profile.html')
    else:
        return redirect('/auth/login')
