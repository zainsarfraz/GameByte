from urllib import request
from django.db.models.fields.files import ImageField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from .models import *
from urllib.request import urlretrieve
from random import randint
from django.core.files.images import ImageFile

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

    return redirect('/googleAuth')

def landingPage(request):
    return render(request,'landing_page.html')