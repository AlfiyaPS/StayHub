from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth

# Create your views here.

def index(request):
    return render(request, "index.html")


def registration(request):
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        password=request.POST['password']
        confirmPassword=request.POST['confirmPassword']
        if CustomUser.objects.filter(username=username).exists():
            messages.info(request,"Username already exists")
            return redirect('registration')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request,"Email already exists")
            return redirect('registration')
        elif password != confirmPassword:
            messages.error(request, "Password and confirmation password do not match")
            return redirect('registration')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password,is_guest=True)
            user.save();
        return redirect('login')
    else:
        return render(request,'registration.html')

def registerproperty(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        property_name = request.POST['property_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        license_upload = request.FILES.get('license_upload')
        

        if (
            CustomUser.objects.filter(username=username).exists()
        ):
            messages.error(request, "User already registered")
            return render(request, "login.html")

        else:
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name = last_name,
                property_name = property_name,
                username=username,
                email=email,
                password=password,
                
                is_host=True,
            )

            user.set_password(password)
            if license_upload:
                user.license_upload = license_upload
                user.save()

            messages.success(request, "Registration successful. You can now login.")
            return redirect("login")

    return render(request, "registerproperty.html")





# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         if email and password:
#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 auth_login(request, user)

#                 if request.user.ROLE_CHOICE==CustomUser.CUSTOMER:
                
#                     return redirect('/')
#                 # elif request.user.user_typ == CustomUser.VENDOR:
#                 #     print("user is therapist")
#                 #     return redirect(reverse('therapist'))
#                 elif request.user.ROLE_CHOICE== CustomUser.DIETITIAN:
#                     print("user is Dietitian")                   
#                     return redirect('d_index')
#                 elif request.user.ROLE_CHOICE== CustomUser.DOCTOR:
#                     print("user is Doctor")                   
#                     return redirect('dr_index')


#                 # else:
#                 #     print("user is normal")
#                 #     return redirect('')

#             else:
#                 messages.success(request,("Invalid credentials."))
#         else:
#             messages.success(request,("Please fill out all fields."))
        
#     return render(request, 'signin.html')


def login(request):
    if request.user.is_authenticated:
        if request.user.is_guest:
            return redirect('guest_dashboard')
        elif request.user.is_host:
            return redirect('host_dashboard')
        

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                if user.is_guest:
                    return redirect('guest_dashboard')
                elif user.is_host:
                    return redirect('host_dashboard')
                
            else:
                error_message = "Invalid login credentials."
                return render(request, "login.html", {"error_message": error_message})

        else:
            error_message = "username and password are required fields."
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")

def host_dashboard(request):
    return render(request,'host_dashboard.html')

def guest_dashboard(request):
    return render(request,'guest_dashboard.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
def services(request):
    return render(request, 'inc/services.html')