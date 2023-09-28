from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html',)
def loginn(request):
    return render(request,'login.html',)
def registration(request):
    return render(request,'registration.html',)
def registerproperty(request):
    return render(request,'registerproperty.html',)