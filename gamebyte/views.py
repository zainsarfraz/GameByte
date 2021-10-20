from django.http import HttpResponse
from django.shortcuts import render


def googleAuthTest(request):
    return render(request,'index.html')