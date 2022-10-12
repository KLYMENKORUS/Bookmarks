from django.contrib import admin
from .models import Profile, Contact


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'profile_photo']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_form', 'user_to', 'created']
