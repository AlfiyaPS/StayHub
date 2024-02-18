from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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
    upload_datetime = models.DateTimeField(default=timezone.now)
    host = models.ForeignKey(
        Host,  # Reference the Host model directly
        on_delete=models.CASCADE,
        related_name='properties', #for adding multiple properties
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

class WishlistItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s wishlist item for {self.property.property_name}"





class Booking(models.Model):
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.IntegerField()
    total_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    num_guests = models.IntegerField(default=0)

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property.property_name} - {self.check_in_date} to {self.check_out_date}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment for Booking {self.booking.booking_id} - {self.amount}"
    
from django.utils.crypto import get_random_string

class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
        

class AddService(models.Model):
    TYPE_CHOICES = [
        ('adventurous', 'Adventurous'),
        ('picnic', 'Picnic'),
        ('cultural', 'Cultural'),
        ('music_concerts', 'Music/Concerts'),
    ]

    service_id = models.CharField(max_length=50, unique=True, editable=False)
    service_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # Duration in minutes
    place = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    service_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='adventurous')
    features = models.ManyToManyField(Feature, related_name='services', blank=True)
    images = models.ImageField(upload_to='service_images/', null=True, blank=True)

    def __str__(self):
        return self.service_name
    
    def save(self, *args, **kwargs):
        # Generate a unique service ID if it doesn't exist
        if not self.service_id:
            unique_id = get_random_string(length=8)
            self.service_id = f'SRV-{unique_id}'
        super().save(*args, **kwargs)
    