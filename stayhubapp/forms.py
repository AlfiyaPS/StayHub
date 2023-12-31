from django import forms
from .models import Host,Guest
from .models import Property
from .models import PropertyImage
from .models import Availability





class HostProfileForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host_first_name', 'host_last_name', 'property_name']
class GuestProfileForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['guest_first_name', 'guest_last_name','phone_number']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_name', 'description', 'location', 'property_type', 'number_of_bedrooms', 'number_of_bathrooms', 'capacity', 'price']

class PropertyImageForm(forms.ModelForm):
    
    class Meta:
        model = PropertyImage
        fields = ['image', 'description']  # Include the description field

    def __init__(self, *args, **kwargs):
        super(PropertyImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class AvailabilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        host = kwargs.pop('host', None)
        host_properties = kwargs.pop('host_properties', None)
        super(AvailabilityForm, self).__init__(*args, **kwargs)

        if host and host_properties:
            self.fields['property'].queryset = host_properties.filter(host=host)

    class Meta:
        model = Availability
        fields = ['property', 'date', 'is_available']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['property', 'check_in_date', 'check_out_date', 'num_guests', 'total_price']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)