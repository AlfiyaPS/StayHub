from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth
from .models import Guest
from .models import Host
from .forms import HostProfileForm, GuestProfileForm

from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyType
from .forms import PropertyForm,PropertyImageForm
from django.forms import modelformset_factory
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from stayhubapp.models import Property, PropertyImage


from .models import Availability
from .forms import AvailabilityForm
# from django.contrib import auth

# Create your views here.

def index(request):
    return render(request, "index.html")


def registration(request):
    if request.method == "POST":
        guest_first_name = request.POST['guest_first_name']
        guest_last_name = request.POST['guest_last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('registration')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('registration')
        elif password != confirm_password:
            messages.error(request, "Password and confirmation password do not match")
            return redirect('registration')
        else:
            user = Guest.objects.create_user(
                guest_first_name=guest_first_name,
                guest_last_name=guest_last_name,
                email=email,
                username=username,
                password=password,
                is_guest=True,
                phone_number=phone_number
            )
            user.role = CustomUser.GUEST  # Set the role to GUEST
            user.save()
        return redirect('login')
    else:
        return render(request, 'registration.html')


def registerproperty(request):
    if request.method == 'POST':
        host_first_name = request.POST['host_first_name']
        host_last_name = request.POST['host_last_name']
        property_name = request.POST['property_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        license_upload = request.FILES.get('license_upload')

        if Host.objects.filter(username=username).exists():
            messages.error(request, "User already registered")
            return render(request, "login.html")

        else:
            user = Host.objects.create_user(
                host_first_name=host_first_name,
                host_last_name=host_last_name,
                email=email,
                username=username,
                password=password,
                property_name=property_name,
            )
            
            user.role = CustomUser.HOST  # Set the role to HOST
            user.set_password(password)
            if license_upload:
                user.license_upload = license_upload
            user.save()

            messages.success(request, "Registration successful. You can now login.")
            return redirect("login")

    return render(request, "registerproperty.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == CustomUser.GUEST:
                if hasattr(user, 'guest') and user.guest.is_guest:
                    # Redirect to the guest dashboard
                    auth_login(request, user)
                    request.session['username'] = username
                    return redirect('guest_dashboard')
                else:
                    messages.error(request, "Invalid role")
            elif user.role == CustomUser.HOST:
                if hasattr(user, 'host') and user.host.is_host:
                    # Check if the host is approved
                    if user.host.approved:
                        # Redirect to the host dashboard
                        auth_login(request, user)
                        request.session['username'] = username
                        return redirect('host_dashboard')
                    else:
                        # Host not approved yet
                        messages.error(request, "Your host account has not been approved yet.")
                else:
                    messages.error(request, "Invalid role")
            elif user.role == CustomUser.ADMIN:
                auth_login(request, user)
                request.session['username'] = username
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid role")
        else:
            # Display the "Invalid login credentials" message when authentication fails
            messages.error(request, "Invalid login credentials")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
    #         messages.error(request, "Invalid username or password")
    # return render(request, "login.html")

#def host_dashboard(request):
  #  if 'username' in request.session:
  #     response = render(request, 'host_dashboard.html')
  #     response['Cache-Control'] = 'no-store, must-revalidate'
  #     return response
  ##  else:
    #   return redirect('/')
    #return render(request,'host_dashboard.html')



@login_required
def host_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'host') and request.user.host.is_host:
        host = request.user.host
        properties = Property.objects.filter(host=host)
        
        # If you have a specific property, you can pass it here
        property = properties.first()  # For example, taking the first property in the list
        
        return render(request, 'host_dashboard.html', {'property': property, 'properties': properties})
    else:
        return redirect('/')

def guest_dashboard(request):
    if 'username' in request.session:
        # Fetch properties along with their associated images
        properties = Property.objects.all()
        property_images = PropertyImage.objects.all()
        return render(request, 'guest_dashboard.html', {'properties': properties, 'property_images': property_images})
    else:
        return redirect('/')

    # return render(request,'guest_dashboard.html')

def logout(request):
    auth(request)
    return redirect('/')
def services(request):
    return render(request, 'inc/services.html')
def admin_dashboard(request):
    if 'username' in request.session:
        # Calculate the number of guests, hosts, and pending approvals
        number_of_guests = Guest.objects.count()
        number_of_hosts = Host.objects.count()
        number_of_pending_approvals = Host.objects.filter(approved=False).count()

        return render(request, 'admin_dashboard.html', {
            'number_of_guests': number_of_guests,
            'number_of_hosts': number_of_hosts,
            'number_of_pending_approvals': number_of_pending_approvals,
        })
    else:
        return redirect('/')


# Add a new view to manage host approvals
@login_required
@user_passes_test(lambda u: u.role == CustomUser.ADMIN)
def manage_host_approvals(request):
    if request.method == 'GET':
        # Fetch all unapproved hosts
        unapproved_hosts = Host.objects.filter(approved=False)
        context = {'unapproved_hosts': unapproved_hosts}
        return render(request, 'manage_host_approvals.html', context)

    if request.method == 'POST':
        host_id = request.POST.get('host_id')
        action = request.POST.get('action')

        # Approve or reject the host based on the action
        host = get_object_or_404(Host, id=host_id)
        if action == 'approve':
            host.approved = True
            host.save()
        elif action == 'reject':
            host.delete()

        return redirect('manage_host_approvals')

    return HttpResponse(status=405)

def view_hosts(request):
    hosts = Host.objects.all()
    return render(request, 'view_hosts.html', {'hosts': hosts})

def view_guests(request):
    guests = Guest.objects.all()
    return render(request, 'view_guests.html', {'guests': guests})

def delete_guest(request, guest_id):
    try:
        guest = Guest.objects.get(id=guest_id)
        guest.delete()
        messages.error(request, 'Guest does not exist')
    except Guest.DoesNotExist:
        
        pass

    return redirect('view_guests')
def delete_host(request, host_id):
    try:
        host = Host.objects.get(id=host_id)
        host.delete()
        messages.error(request, 'Host Deleted Successfully')
    except Host.DoesNotExist:
        
        pass

    return redirect('view_hosts')

def edit_host_profile(request):
    host = request.user.host  # Retrieve the host object of the logged-in user

    if request.method == 'POST':
        form = HostProfileForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            return redirect('host_profile')  # Redirect to the host profile after a successful update
    else:
        form = HostProfileForm(instance=host)

    context = {'form': form}
    return render(request, 'edit_host_profile.html', context)

@login_required
def edit_guest_profile(request):
    guest = request.user.guest

    if request.method == 'POST':
        form = GuestProfileForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('guest_profile')  # Redirect to the profile page
    else:
        form = GuestProfileForm(instance=guest)

    return render(request, 'edit_guest_profile.html', {'form': form})

def host_profile(request):
    host = request.user.host  # Retrieve the host object of the logged-in user
    context = {'host': host}
    return render(request, 'host_profile.html', context)
@login_required

def guest_profile(request):
    guest = request.user.guest
    return render(request, 'guest_profile.html', {'guest': guest})
        
  
@login_required
def add_property(request):
    ImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=5, max_num=6)

    if request.method == 'POST':
        form = PropertyForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if form.is_valid() and image_formset.is_valid():
            property = form.save(commit=False)
            property.host = request.user.host
            property.save()

            for idx, image_form in enumerate(image_formset):
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.property = property
                    image.save()

                    # Set the first uploaded image as the cover photo
                    if idx == 0:
                        property.cover_photo = image
                        property.save()

            return redirect('view_property', property_id=property.property_id)
    else:
        host = request.user.host
        initial_data = {'property_name': host.property_name}
        form = PropertyForm(initial=initial_data)
        image_formset = ImageFormSet(queryset=PropertyImage.objects.none())

    return render(request, 'add_property.html', {'form': form, 'image_formset': image_formset})


def view_property(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    images = property.propertyimage_set.all()  # Retrieve all related images for the property
    return render(request, 'view_property.html', {'property': property, 'images': images})

def edit_property(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        image_form = PropertyImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
        # Check if an image was provided before attempting to save it
        if 'image' in request.FILES:
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.property = property
                image.save()

        return redirect('view_property', property_id=property.property_id)
    else:
        form = PropertyForm(instance=property)
        image_form = PropertyImageForm()

    return render(request, 'edit_property.html', {'form': form, 'image_form': image_form, 'property': property})


@login_required
def add_availability(request, property_id):
    property = Property.objects.get(pk=property_id)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            form.instance.property = property
            form.save()
            return redirect('add_availability', property_id=property_id)

    else:
        form = AvailabilityForm()

    availabilities = Availability.objects.filter(property=property)
    return render(request, 'add_availability.html', {
        'property': property,
        'form': form,
        'availabilities': availabilities,
    })

def guest_property_details(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    images = PropertyImage.objects.filter(property=property)
    
    # Initialize host information with default values
    host_first_name = "No Host Information Available"
    host_last_name = ""

    if property.host and property.host.is_host:
        host_first_name = property.host.host_first_name
        host_last_name = property.host.host_last_name

    context = {
        'property': property,
        'images': images,
        'host_first_name': host_first_name,
        'host_last_name': host_last_name,
    }

    return render(request, 'guest_property_details.html', context)

def search_properties(request):
    name = request.GET.get('name')
    location = request.GET.get('location')

    properties = Property.objects.filter(property_name__icontains=name, location__icontains=location)


    return render(request, 'search_results.html', {'properties': properties})

def add_to_wishlist(request, property_id):
    if request.user.is_authenticated:
        property = get_object_or_404(Property, property_id=property_id)
        user = request.user
        # Check if the property is not already in the user's wishlist
        if not WishlistItem.objects.filter(user=user, property=property).exists():
            wishlist_item = WishlistItem(user=user, property=property)
            wishlist_item.save()
        # You can redirect to the 'view_wishlist' view after adding to the wishlist.
        return redirect('view_wishlist')
    # Handle the case where the user is not authenticated
    # You can add your own logic for this case, such as redirecting to a login page.
    return redirect('login')  # Example: redirect to the login page

def view_wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist_items = WishlistItem.objects.filter(user=user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

def remove_from_wishlist(request, property_id):
    if request.user.is_authenticated:
        property = get_object_or_404(Property, property_id=property_id)
        user = request.user
        # Check if the property is in the user's wishlist and remove it
        wishlist_item = WishlistItem.objects.filter(user=user, property=property)
        if wishlist_item.exists():
            wishlist_item.delete()
        # Redirect back to the wishlist page
        return redirect('view_wishlist')
    # Handle the case where the user is not authenticated
    # You can add your own logic for this case, such as redirecting to a login page.
    return redirect('login')  # Example: redirect to the login page