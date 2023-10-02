from django.contrib import admin
from django.urls import path
from.import views
urlpatterns = [
    path('',views.index,name="home"),
    path('login/',views.login,name="login"),
    path('registration/',views.registration,name="registration"),
    path('registerproperty/',views.registerproperty,name="registerproperty"),
    path('host_dashboard/',views.host_dashboard,name="host_dashboard"),
    path('guest_dashboard/',views.guest_dashboard,name="guest_dashboard"),
    path('logout/',views.logout,name="logout"),
    path('services/', views.services, name='services'),

]
