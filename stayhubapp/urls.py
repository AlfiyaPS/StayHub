from django.contrib import admin
from django.urls import path
from.import views
urlpatterns = [
    path('',views.index,name="home"),
    path('login/',views.loginn,name="login"),
    path('registration/',views.registration,name="registration"),
    path('registerproperty/',views.registerproperty,name="registerproperty"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('logout/',views.logout,name="logout"),

]