from django.shortcuts import render,redirect
from .forms import signupForm,notesForm,updateForm,feedbackForm
from .models import user_signup
from django.contrib.auth import logout
from django.core.mail import send_mail
from NotesApp import settings
import requests
import random

# Create your views here.

def index(request):
    if request.method=='POST': #root
        if request.POST.get('signup')=='signup':
            newuser=signupForm(request.POST)
            if newuser.is_valid():
                newuser.save()
                print("Signup successfully!")
            else:
                print(newuser.errors)
        elif request.POST.get("login")=="login":
            unm=request.POST['username']
            pas=request.POST['password']

            uid=user_signup.objects.get(username=unm)
            print("Current User:",uid.id)
            user=user_signup.objects.filter(username=unm,password=pas)
            if user: #true
                print("Login Successfully!")


                # MSG Sending Code
                otp=random.randint(1111,9999)
                url = "https://www.fast2sms.com/dev/bulkV2"
                querystring = {"authorization":"PSqGhvu5BkQv1WEvvWH6PIgV0vr1IcOIEzgsN1fZMHFG0WJapJ1hGGIwYfq8","variables_values":f"{otp}","route":"otp","numbers":"7069604925,8849906669,9313078908,7777945889,9773013554,6353231368,9429990451,9662665836"}
                headers = {
                    'cache-control': "no-cache"
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)    

                request.session['user']=unm #create session
                request.session['userid']=uid.id
                return redirect('notes')
            else:
                print("Error! Login fail")
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        newnotes=notesForm(request.POST,request.FILES)
        if newnotes.is_valid():
            newnotes.save()
            print("Your notes has been uploaded!")
        else:
            print(newnotes.errors)
    return render(request,'notes.html',{'user':user})

def contact(request):
    if request.method=='POST':
        newfeedback=feedbackForm(request.POST)
        if newfeedback.is_valid():
            newfeedback.save()
            print("Your feedback has been sent!")

            #Email Sending Code
            #send_mail(subject="Thank you!",message=f"Dear User\nWe got your feedback,\nThank you for your interest.\nNeed any help, \nContact us on +91 9724799469 | sanket@gmail.com",from_email=settings.EMAIL_HOST_USER,recipient_list=['komaldarjiv@gmail.com','jotangiyabinal17@gmail.com','nenshibhanderi885@gmail.com','asodariyarutvi@gmail.com','adimandaliya03@gmail.com','smitbhatti30@gmail.com','patelbhumil8666@gmail.com'])
            sub="Thank you!"
            msg=f"Dear User\nWe got your feedback,\nThank you for your interest.\nNeed any help, \nContact us on +91 9724799469 | sanket@gmail.com"
            from_ID=settings.EMAIL_HOST_USER
            to_ID=[request.POST['email']]
            send_mail(subject=sub,message=msg,from_email=from_ID,recipient_list=to_ID)

        else:
            print(newfeedback.errors)
    return render(request,'contact.html')
    
def profile(request):
    user=request.session.get('user')
    uid=request.session.get('userid')
    cuser=user_signup.objects.get(id=uid)
    if request.method=='POST':
        updateuser=updateForm(request.POST)
        if updateuser.is_valid():
            updateuser=updateForm(request.POST,instance=cuser)
            updateuser.save()
            print("Your profile has been updated!")
        else:
            print(updateuser.errors)
    return render(request,'profile.html',{'user':user,'cuser':user_signup.objects.get(id=uid)})

def userlogout(request):
    logout(request)
    return redirect('/')
