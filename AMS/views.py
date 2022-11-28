from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import save
from PROJECT import settings
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request,'AMS/index.html')


def signup(request):
    
    if request.method == "POST":
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try another")
            
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect(home)
        
        if len(username)>10:
            messages.error(request, "username must be under 10 characters")
            return redirect(home)
            
        if pass1!=pass2:
            messages.error(request,"Password didn't match")
            return redirect(home)
            
        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric")
            return redirect(home)
        
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        
        myuser.save()
        
        messages.success(request, "Your Account has been successfully created")
        
        
        subject="Welcome to Admin pannel"
        message="Hello"+myuser.first_name + "!!\n"+ "welcome to Admin pannel !!\n Thanks for visiting admin pannel\n we have sent you a confirmation mail, please confirm your email address in order to active your account.\n\n Thank You😎😎\n {{fname}}"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message, from_email, to_list, fail_silently=True)
        
        
        
        return redirect('signin')
    
    
    return render(request,'AMS/signup.html')

def signin(request):
    
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass1')

        user=authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname=user.first_name
            return render(request, "AMS/index.html", {'fname':fname})
            
        else:
            messages.error(request, "Bed Credential")
            return redirect('home')
        
    return render(request,'AMS/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out succesfully")
    return redirect('home')