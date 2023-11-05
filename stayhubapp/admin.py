from django.contrib import admin
from .models import CustomUser, Guest, Host
from django.utils.translation import gettext as _
from .models import Property, PropertyType

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Guest)
admin.site.register(Host)

admin.site.register(Property)
admin.site.register(PropertyType)