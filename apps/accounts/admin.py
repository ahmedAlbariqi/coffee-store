from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'is_default')
    search_fields = ('user__username', 'full_name', 'city')
    list_filter = ('city', 'is_default')
