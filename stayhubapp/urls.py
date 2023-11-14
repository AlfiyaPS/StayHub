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
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('view_hosts/', views.view_hosts, name='view_hosts'),
    path('view_guests/', views.view_guests, name='view_guests'),
    path('delete_guest/<int:guest_id>/', views.delete_guest, name='delete_guest'),
    path('delete_host/<int:host_id>/', views.delete_host, name='delete_host'),

    path('edit-host-profile/', views.edit_host_profile, name='edit_host_profile'),
    path('edit-guest-profile/', views.edit_guest_profile, name='edit_guest_profile'),
    path('host/profile/', views.host_profile, name='host_profile'),
    path('guest_profile/', views.guest_profile, name='guest_profile'),
    path('add_property/', views.add_property, name='add_property'),
    path('view_property/<int:property_id>/', views.view_property, name='view_property'),
    path('edit_property/<int:property_id>/', views.edit_property, name='edit_property'),

    path('manage_host_approvals/', views.manage_host_approvals, name='manage_host_approvals'),    
    
    path('add_availability/<int:property_id>/', views.add_availability, name='add_availability'),


   

    path('property/<int:property_id>/', views.guest_property_details, name='guest_property_details'),

    path('search/', views.search_properties, name='search_properties'),
    
    path('add_to_wishlist/<int:property_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('remove_from_wishlist/<int:property_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]

