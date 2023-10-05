from django.contrib import admin
from django.urls import path
from.import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView


 
urlpatterns = [
    path('',views.index,name="home"),
    path('login/',views.login,name="login"),
    path('registration/',views.registration,name="registration"),
    path('registerproperty/',views.registerproperty,name="registerproperty"),
    path('host_dashboard/',views.host_dashboard,name="host_dashboard"),
    path('guest_dashboard/',views.guest_dashboard,name="guest_dashboard"),
    path('logout/',views.logout,name="logout"),
    path('services/', views.services, name='services'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete')

]
