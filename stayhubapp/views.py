from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth
# from django.contrib import auth

# Create your views here.

def index(request):
    return render(request, "index.html")


def registration(request):
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        phone_number=request.POST['phone']
        password=request.POST['password']
        confirm_password = request.POST['confirm_password']

        if CustomUser.objects.filter(username=username).exists():
            messages.info(request,"Username already exists")
            return redirect('registration')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request,"Email already exists")
            return redirect('registration')
        elif password != confirm_password:
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['username'] = username
            if user.is_staff:
                return redirect('admin_dashboard')
            elif user.is_guest:
                return redirect('guest_dashboard')
            elif user.is_host:
                return redirect('host_dashboard')
        else:
            messages.error(request, "Invalid login credentials")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
            
           
           
           
           
           
           
           
    #         messages.error(request, "Invalid username or password")
    # return render(request, "login.html")

def host_dashboard(request):
    if 'username' in request.session:
       response = render(request, 'host_dashboard.html')
       response['Cache-Control'] = 'no-store, must-revalidate'
       return response
    else:
       return redirect('/')
    #return render(request,'host_dashboard.html')

def guest_dashboard(request):
    if 'username' in request.session:
       response = render(request, 'guest_dashboard.html')
       response['Cache-Control'] = 'no-store, must-revalidate'
       return response
    else:
       return redirect('/')



    # return render(request,'guest_dashboard.html')

def logout(request):
    auth(request)
    return redirect('/')
def services(request):
    return render(request, 'inc/services.html')
def admin_dashboard(request):
    if 'username' in request.session:
       response = render(request, 'admin_dashboard.html')
       response['Cache-Control'] = 'no-store, must-revalidate'
       return response
    else:
       return redirect('/')
    #return render(request,'admin_dashboard.html')