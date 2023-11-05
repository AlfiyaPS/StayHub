from django.db import models
from django.contrib.auth import get_user_model


from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GUEST = 1
    HOST = 2
    ADMIN = 3
    
    ROLE_CHOICE = (
        (GUEST, 'guest'),
        (HOST, 'host'),
        (ADMIN, 'admin'),
    )
    
    username = models.CharField(max_length=100, unique=True, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, default=GUEST)
    
    # Common fields for both Guest and Host
    property_name = models.CharField(max_length=255, default='')

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Guest(CustomUser):
    is_guest = models.BooleanField(default=True)
    is_host = models.BooleanField(default=False)
    
    # Fields specific to guests
    guest_first_name = models.CharField(max_length=30)
    guest_last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.guest_first_name} {self.guest_last_name}"
    
class Host(CustomUser):
    is_guest = models.BooleanField(default=False)
    is_host = models.BooleanField(default=True)
    approved = models.BooleanField(null=True, default=False)
    
    host_first_name = models.CharField(max_length=100)
    host_last_name = models.CharField(max_length=100)
    license_upload = models.FileField(upload_to='licenses/')
    def __str__(self):
        return f"{self.host_first_name} {self.host_last_name}"
    #def __str__(self):
        #return self.username

class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    property_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    number_of_bedrooms = models.PositiveIntegerField()
    number_of_bathrooms = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    host = models.ForeignKey(
        Host,  # Reference the Host model directly
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.property_name


    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    description = models.TextField(blank=True)  # Add a description field

    def __str__(self):
        return f"Image for {self.property.property_name}"

class Availability(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)