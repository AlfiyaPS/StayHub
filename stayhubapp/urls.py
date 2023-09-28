from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('login/',views.loginn,name="login"),
    path('registration/',views.registration,name="registration"),
    path('registerproperty/',views.registerproperty,name="registerproperty"),
    

]
