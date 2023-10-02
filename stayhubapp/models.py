from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    GUEST = 1
    HOST = 2
    

    ROLE_CHOICE = (
     (GUEST, 'guest'),
     (HOST, 'host'),
     
    )
    #username = None
    username = models.CharField(max_length=100,unique=True ,default='')
    #first_name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    property_name = models.CharField(max_length=255, default='')
    #role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default=CUSTOMER)
    is_guest = models.BooleanField(default=False ,blank=True)
    is_host = models.BooleanField(default=False)
    
    
    REQUIRED_FIELDS = ['email']  # Add any additional required fields here
    USERNAME_FIELD = 'username'
        
    # def str(self):
    #     return self.username
