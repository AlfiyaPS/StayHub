from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

def loginn(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/dashboard')
        else:
            messages.info(request,"Invalid login")
            return redirect('login')
        
    return render(request,'login.html')


def registration(request):
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        password=request.POST['password']
        confirmPassword=request.POST['confirmPassword']
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already exists")
            return redirect('registration')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email already exists")
            return redirect('registration')
        elif password != confirmPassword:
            messages.error(request, "Password and confirmation password do not match")
            return redirect('registration')
        else:
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.save();
        return redirect('login')
    else:
        return render(request,'registration.html')
    
def registerproperty(request):
    return render(request,'registerproperty.html')

def dashboard(request):
    return render(request,'dashboard.html')

def logout(request):
    auth.logout(request)
    return redirect('/')