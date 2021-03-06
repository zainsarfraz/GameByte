from urllib import request
from django.db.models.fields.files import ImageField
from django.http import HttpResponse
from django.http.response import JsonResponse
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
import datetime

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

    return redirect('/dashboard')

def landingPage(request):
    if not request.user.is_authenticated:
        return render(request,'landing_page.html')
    else:
        return redirect('/dashboard')


def check_email(request):
    email = request.POST.get('email', None)
    if User.objects.filter(email=email).exists():
        return HttpResponse("true")
    else:
        return HttpResponse("false")

def check_username(request):
    username = request.POST.get('username', None)
    if User.objects.filter(username=username).exists():
        return HttpResponse("true")
    else:
        return HttpResponse("false")

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
    else:
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            return render(request,'registration/signup.html')


def playground(request,id):
    if request.user.is_authenticated:
        problem = Problem.objects.get(id=id)
        f = open('templates/'+problem.templateSolutionCode,'r')
        templateSolutionCode = f.read()
        #print(templateSolutionCode)
        # check for a query parameter
        try:
            if request.GET['submission_id'] is not None:
                submission = Submission.objects.get(id=request.GET['submission_id'])
                # read submission file 
                filename = 'static/attempts/'+submission.user_id.username+'_'+str(submission.id)+'.py'
                file = open(filename,'r')
                code = file.read()
                file.close()
                return render(request,'playground.html',{'problem':problem,'templateSolutionCode':code})
        except Exception as e:
            print(e)
            
        return render(request,'playground.html',{'problem':problem,'templateSolutionCode':templateSolutionCode})
    else:
        return redirect('/auth/login')

def dashboard(request):
    if request.user.is_authenticated:
        problems = Problem.objects.all()
        submissions = Submission.objects.filter(user_id=request.user.id)
        print(submissions)
        return render(request,'dashboard.html',{'problems':problems,'submissions':submissions})
        
    else:
        return redirect('/auth/login')

def problems(request):
    if request.user.is_authenticated:
        problems = Problem.objects.all()
        return render(request,'problems.html',{'problems':problems})
    else:
        return redirect('/auth/login')


def user_profile(request):
    if request.user.is_authenticated:
        userDetails = UserDetails.objects.get(user_id=request.user.id)
        return render(request,'user_profile.html',{'userDetails':userDetails})
    else:
        return redirect('/auth/login')

def about(request):
    if request.user.is_authenticated:
        return render(request,'about.html')
    else:
        return redirect('/auth/login')

def runtestcase(request):
    if request.user.is_authenticated:

        code = request.POST.get('code', None)
        problem_id = request.POST.get('problem_id', None)
        argumentsString = request.POST.get('arguments', None)
        argumentsString = argumentsString[1:-1]
        arguments = argumentsString.split(',')
        # creating code file
        filename = 'static/attempts/'+request.user.username+'_'+str(problem_id)+'.py'
        file = open(filename,'w')
        file.write('#!/usr/bin/env python\n')
        for i in code:
            file.write(str(i))
        file.close()


        args = ""
        for argument in arguments:
            args += str(argument)+","
        args = args[:-1]    

        result = ""
        errorFlag = False
        errorMessage = ""

        import subprocess
        args = args.encode('utf-8')
        try:

            # deployed code
            import sys
            if 'runserver' in sys.argv:
                proc = subprocess.Popen(
                'python ' + filename +'',stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            else:
                import os
                import stat
                st = os.stat(filename)
                os.chmod(filename, st.st_mode | stat.S_IEXEC)
                proc = subprocess.Popen(
                    [sys.executable,filename],stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            proc.stdin.write(args)
            #proc.stdin.close()
            output,error = proc.communicate()
            
            if error != b'':
                errorFlag = True
                errorMessage = error.decode('utf-8')
            if output != b'':
                errorFlag = False         
            result = output
            result = result.decode('utf-8')
            proc.wait()
        except Exception as e:
            print(e)
            errorMessage = str(e)
            errorFlag = True

        
        return JsonResponse({'result':result,'error':errorFlag,'message':errorMessage})
    else:
        return redirect('/auth/login')
def submitcode(request):
    if request.user.is_authenticated:
        code = request.POST.get('code', None)
        problem_id = request.POST.get('problem_id', None)
        problem = Problem.objects.get(id=problem_id)
        submission = Submission(user_id=request.user,problem_id=problem,submission_code=code,submission_language='python')
        submission.save()
        # get the submission id
        submission_id = submission.id
        # make code file and save in server
        filename = 'static/attempts/'+request.user.username+'_'+str(submission_id)+'.py'
        file = open(filename,'w')
        for i in code:
            file.write(str(i))
        file.close()
        
        return JsonResponse({'result':'success'})

def update_profile(request):
    if request.user.is_authenticated:
        about = request.POST.get('about', None)
        company = request.POST.get('company', None)
        education = request.POST.get('education', None)
        programming_language = request.POST.get('programming_languages', None)
        skills =    request.POST.get('skills', None)
        country = request.POST.get('country', None)
        user_details = UserDetails.objects.get(user_id=request.user)
        user_details.bio = about
        user_details.company = company
        user_details.education = education
        user_details.programming_languages = programming_language
        user_details.skills = skills
        user_details.country = country
        user_details.save()
        return JsonResponse({'result':'success'})
    else:
        return redirect('/auth/login')


def submissions(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.all()
        # sort by date
        submissions = sorted(submissions, key=lambda x: x.submission_time, reverse=True)
        return render(request,'submissions.html',{'submissions':submissions})

def downloadCode(request,id):
    if request.user.is_authenticated:
        submission = Submission.objects.get(id=id)
        filename = 'static/attempts/'+submission.user_id.username+'_'+str(submission.id)+'.py'
        file = open(filename,'r')
        code = file.read()
        file.close()
        response = HttpResponse(code, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=code.py'
        return response

def runCode(request,id):
    submission = Submission.objects.get(id=id)
    return redirect('/playground/'+str(submission.problem_id.id)+'?submission_id='+str(submission.id))