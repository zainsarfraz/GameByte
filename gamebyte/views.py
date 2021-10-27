from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail


def googleAuthTest(request):
    print(request.user)
    return render(request,'index.html')